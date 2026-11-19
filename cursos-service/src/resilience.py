import requests


class DependencyError(Exception):
    """Falla controlada al comunicarse con otro microservicio."""

    def __init__(self, message, status):
        super().__init__(message)
        self.message = message
        self.status = status


def call_service(service_name, url, timeout):
    """
    Hace un GET a otro servicio con un tiempo máximo de espera.
    Un 404 es una respuesta válida y se devuelve al llamador;
    los errores de red y las respuestas 5xx se convierten en DependencyError.
    """
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code >= 500:
            response.raise_for_status()
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
