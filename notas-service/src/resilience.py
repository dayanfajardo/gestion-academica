import math
import os
from datetime import datetime, timedelta, timezone

import pybreaker
import requests


class DependencyError(Exception):
    """Falla controlada al comunicarse con otro microservicio."""

    def __init__(self, message, status):
        super().__init__(message)
        self.message = message
        self.status = status


class RegistroCircuito(pybreaker.CircuitBreakerListener):
    """Escribe en los logs del contenedor cada cambio de estado del circuito."""

    def state_change(self, cb, old_state, new_state):
        anterior = old_state.name.upper().replace('-', '_') if old_state else 'NINGUNO'
        nuevo = new_state.name.upper().replace('-', '_')
        print(f'[circuit breaker {cb.name}] {anterior} -> {nuevo}', flush=True)


def create_breaker(name):
    """Crea un circuit breaker configurado por variables de entorno."""
    return pybreaker.CircuitBreaker(
        fail_max=int(os.getenv('CB_MAX_FALLOS', '3')),
        reset_timeout=int(os.getenv('CB_RECUPERACION', '30')),
        throw_new_error_on_trip=False,
        listeners=[RegistroCircuito()],
        name=name
    )


def call_service(breaker, service_name, url, timeout):
    try:
        with breaker.calling():
            response = requests.get(url, timeout=timeout)
            if response.status_code >= 500:
                response.raise_for_status()
    except pybreaker.CircuitBreakerError:
        raise DependencyError(
            f'Circuito abierto: el servicio de {service_name} no será consultado.', 503)
    except requests.exceptions.Timeout:
        raise DependencyError(
            f'Tiempo de espera agotado al consultar el servicio de {service_name}.', 504)
    except requests.exceptions.ConnectionError:
        raise DependencyError(
            f'No se pudo conectar con el servicio de {service_name}.', 503)
    except requests.exceptions.HTTPError:
        raise DependencyError(
            f'El servicio de {service_name} respondió con un error.', 502)

    return response


def breaker_status(breaker):
    estado = breaker.current_state.upper().replace('-', '_')
    segundos_restantes = 0
    opened_at = breaker._state_storage.opened_at
    if estado == 'OPEN' and opened_at:
        reintento = opened_at + timedelta(seconds=breaker.reset_timeout)
        segundos_restantes = max(0, math.ceil((reintento - datetime.now(timezone.utc)).total_seconds()))
        if segundos_restantes == 0:
            estado = 'HALF_OPEN'

    return {
        'estado_circuito': estado,
        'segundos_para_half_open': segundos_restantes,
        'fallos_consecutivos': breaker.fail_counter,
        'max_fallos': breaker.fail_max,
        'periodo_recuperacion': breaker.reset_timeout
    }
