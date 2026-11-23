import os

import pybreaker
import requests


class DependencyError(Exception):
    """Falla controlada al comunicarse con otro microservicio."""

    def __init__(self, message, status):
        super().__init__(message)
        self.message = message
        self.status = status


def create_breaker(name):
    """Crea un circuit breaker configurado por variables de entorno."""
    return pybreaker.CircuitBreaker(
        fail_max=int(os.getenv('CB_MAX_FALLOS', '3')),
        reset_timeout=int(os.getenv('CB_RECUPERACION', '30')),
        throw_new_error_on_trip=False,
        name=name
    )


def call_service(breaker, service_name, url, timeout):
    """
    Hace un GET a otro servicio protegido por timeout y circuit breaker.
    Solo los errores de red y las respuestas 5xx cuentan como fallo del circuito;
    un 404 es una respuesta válida y se devuelve al llamador.
    """
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
    """Estado actual del circuito, para el endpoint de monitoreo."""
    return {
        'estado_circuito': breaker.current_state.upper(),
        'fallos_consecutivos': breaker.fail_counter,
        'max_fallos': breaker.fail_max,
        'periodo_recuperacion': breaker.reset_timeout
    }
