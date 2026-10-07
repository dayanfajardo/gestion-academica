// El frontend solo habla con el API Gateway.
const API_URL = 'http://localhost:8000';

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', iniciarApp);
} else {
  iniciarApp();
}

function iniciarApp() {
  document.querySelectorAll('[data-vista]').forEach(function (elemento) {
    elemento.addEventListener('click', function () {
      mostrarVista(elemento.getAttribute('data-vista'));
    });
  });

  document.getElementById('form-docente').addEventListener('submit', guardarDocente);
  document.getElementById('form-curso').addEventListener('submit', guardarCurso);
  document.getElementById('form-estudiante').addEventListener('submit', guardarEstudiante);
  document.getElementById('form-matricula').addEventListener('submit', guardarMatricula);
  document.getElementById('form-nota').addEventListener('submit', guardarNota);

  document.getElementById('cancelar-docente').addEventListener('click', limpiarFormularioDocente);
  document.getElementById('cancelar-curso').addEventListener('click', limpiarFormularioCurso);
  document.getElementById('cancelar-estudiante').addEventListener('click', limpiarFormularioEstudiante);
  document.getElementById('cancelar-matricula').addEventListener('click', limpiarFormularioMatricula);
  document.getElementById('cancelar-nota').addEventListener('click', limpiarFormularioNota);

  mostrarVista('inicio');
}

function mostrarVista(nombre) {
  document.querySelectorAll('.vista').forEach(function (vista) {
    vista.classList.add('oculta');
  });
  document.getElementById('vista-' + nombre).classList.remove('oculta');

  document.querySelectorAll('.menu button').forEach(function (boton) {
    boton.classList.toggle('enlace-activo', boton.getAttribute('data-vista') === nombre);
  });

  ocultarAlerta();

  if (nombre === 'docentes') {
    cargarDocentes();
  }
  if (nombre === 'cursos') {
    cargarCursos();
  }
  if (nombre === 'estudiantes') {
    cargarEstudiantes();
  }
  if (nombre === 'matriculas') {
    cargarMatriculas();
  }
  if (nombre === 'notas') {
    cargarNotas();
  }
}

// Envía la petición al Gateway y convierte la respuesta a JSON.
async function pedirAlGateway(ruta, opciones) {
  const configuracion = opciones || {};
  const respuesta = await fetch(API_URL + ruta, {
    method: configuracion.method || 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
    body: configuracion.body ? JSON.stringify(configuracion.body) : undefined
  });

  const texto = await respuesta.text();
  let datos = null;
  try {
    datos = texto ? JSON.parse(texto) : null;
  } catch (error) {
    datos = { error: 'El servidor no devolvió una respuesta válida.' };
  }

  return {
    ok: respuesta.ok,
    datos: datos
  };
}

function mensajeDelServidor(datos) {
  if (!datos) {
    return 'Ocurrió un error inesperado.';
  }
  return datos.message || datos.error || datos.mensaje || 'Ocurrió un error inesperado.';
}

function mostrarAlerta(texto, tipo) {
  const alerta = document.getElementById('alerta');
  alerta.textContent = texto;
  alerta.className = 'alerta ' + (tipo === 'ok' ? 'alerta-ok' : 'alerta-error');
}

function ocultarAlerta() {
  const alerta = document.getElementById('alerta');
  alerta.className = 'alerta oculta';
  alerta.textContent = '';
}

function buscarPorId(lista, id) {
  return lista.find(function (item) {
    return String(item.id) === String(id);
  });
}

function textoOpcionVacia(texto) {
  return '<option value="">' + texto + '</option>';
}

/* ---------- DOCENTES ---------- */

async function cargarDocentes() {
  const resultado = await pedirAlGateway('/docentes');
  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }
  dibujarTablaDocentes(resultado.datos);
}

function dibujarTablaDocentes(docentes) {
  const cuerpo = document.getElementById('tabla-docentes');
  if (!docentes.length) {
    cuerpo.innerHTML = '<tr><td colspan="7" class="vacio">No hay docentes registrados.</td></tr>';
    return;
  }

  cuerpo.innerHTML = docentes.map(function (docente) {
    return (
      '<tr>' +
      '<td>' + docente.id + '</td>' +
      '<td>' + docente.cedula + '</td>' +
      '<td>' + docente.nombre + '</td>' +
      '<td>' + docente.correo + '</td>' +
      '<td>' + docente.departamento + '</td>' +
      '<td>' + (docente.genero || '') + '</td>' +
      '<td>' +
      '<button type="button" class="boton boton-pequeno" onclick="editarDocente(' + docente.id + ')">Editar</button>' +
      '<button type="button" class="boton boton-pequeno boton-peligro" onclick="eliminarDocente(' + docente.id + ')">Eliminar</button>' +
      '</td>' +
      '</tr>'
    );
  }).join('');
}

async function guardarDocente(evento) {
  evento.preventDefault();
  const id = document.getElementById('docente-id').value;
  const cuerpo = {
    cedula: document.getElementById('docente-cedula').value,
    nombre: document.getElementById('docente-nombre').value,
    correo: document.getElementById('docente-correo').value,
    departamento: document.getElementById('docente-departamento').value,
    genero: document.getElementById('docente-genero').value
  };

  const ruta = id ? '/docentes/' + id : '/docentes';
  const resultado = await pedirAlGateway(ruta, {
    method: id ? 'PUT' : 'POST',
    body: cuerpo
  });

  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }

  mostrarAlerta(mensajeDelServidor(resultado.datos), 'ok');
  limpiarFormularioDocente();
  cargarDocentes();
}

async function editarDocente(id) {
  const resultado = await pedirAlGateway('/docentes/' + id);
  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }
  const docente = resultado.datos;
  document.getElementById('docente-id').value = docente.id;
  document.getElementById('docente-cedula').value = docente.cedula;
  document.getElementById('docente-nombre').value = docente.nombre;
  document.getElementById('docente-correo').value = docente.correo;
  document.getElementById('docente-departamento').value = docente.departamento;
  document.getElementById('docente-genero').value = docente.genero || '';
}

async function eliminarDocente(id) {
  if (!confirm('¿Eliminar este docente?')) {
    return;
  }
  const resultado = await pedirAlGateway('/docentes/' + id, { method: 'DELETE' });
  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }
  mostrarAlerta(mensajeDelServidor(resultado.datos), 'ok');
  cargarDocentes();
}

function limpiarFormularioDocente() {
  document.getElementById('form-docente').reset();
  document.getElementById('docente-id').value = '';
}

/* ---------- CURSOS ---------- */

async function cargarCursos() {
  const docentes = await pedirAlGateway('/docentes');
  const cursos = await pedirAlGateway('/cursos');

  if (!docentes.ok) {
    mostrarAlerta(mensajeDelServidor(docentes.datos), 'error');
    return;
  }
  if (!cursos.ok) {
    mostrarAlerta(mensajeDelServidor(cursos.datos), 'error');
    return;
  }

  llenarSelectDocentes(docentes.datos);
  dibujarTablaCursos(cursos.datos, docentes.datos);
}

function llenarSelectDocentes(docentes) {
  const select = document.getElementById('curso-docente');
  const valorActual = select.value;
  select.innerHTML = textoOpcionVacia('Seleccione un docente');
  docentes.forEach(function (docente) {
    const opcion = document.createElement('option');
    opcion.value = docente.id;
    opcion.textContent = docente.nombre + ' (ID ' + docente.id + ')';
    select.appendChild(opcion);
  });
  if (valorActual) {
    select.value = valorActual;
  }
}

function dibujarTablaCursos(cursos, docentes) {
  const cuerpo = document.getElementById('tabla-cursos');
  if (!cursos.length) {
    cuerpo.innerHTML = '<tr><td colspan="7" class="vacio">No hay cursos registrados.</td></tr>';
    return;
  }

  cuerpo.innerHTML = cursos.map(function (curso) {
    const docente = buscarPorId(docentes, curso.docente_id);
    const nombreDocente = docente ? docente.nombre : 'ID ' + curso.docente_id;
    return (
      '<tr>' +
      '<td>' + curso.id + '</td>' +
      '<td>' + curso.codigo + '</td>' +
      '<td>' + curso.nombre + '</td>' +
      '<td>' + curso.creditos + '</td>' +
      '<td>' + curso.semestre + '</td>' +
      '<td>' + nombreDocente + '</td>' +
      '<td>' +
      '<button type="button" class="boton boton-pequeno" onclick="editarCurso(' + curso.id + ')">Editar</button>' +
      '<button type="button" class="boton boton-pequeno boton-peligro" onclick="eliminarCurso(' + curso.id + ')">Eliminar</button>' +
      '</td>' +
      '</tr>'
    );
  }).join('');
}

async function guardarCurso(evento) {
  evento.preventDefault();
  const id = document.getElementById('curso-id').value;
  const cuerpo = {
    codigo: document.getElementById('curso-codigo').value,
    nombre: document.getElementById('curso-nombre').value,
    creditos: Number(document.getElementById('curso-creditos').value),
    semestre: Number(document.getElementById('curso-semestre').value),
    docente_id: Number(document.getElementById('curso-docente').value)
  };

  const ruta = id ? '/cursos/' + id : '/cursos';
  const resultado = await pedirAlGateway(ruta, {
    method: id ? 'PUT' : 'POST',
    body: cuerpo
  });

  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }

  mostrarAlerta(mensajeDelServidor(resultado.datos), 'ok');
  limpiarFormularioCurso();
  cargarCursos();
}

async function editarCurso(id) {
  const resultado = await pedirAlGateway('/cursos/' + id);
  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }
  const curso = resultado.datos;
  document.getElementById('curso-id').value = curso.id;
  document.getElementById('curso-codigo').value = curso.codigo;
  document.getElementById('curso-nombre').value = curso.nombre;
  document.getElementById('curso-creditos').value = curso.creditos;
  document.getElementById('curso-semestre').value = curso.semestre;
  document.getElementById('curso-docente').value = curso.docente_id;
}

async function eliminarCurso(id) {
  if (!confirm('¿Eliminar este curso?')) {
    return;
  }
  const resultado = await pedirAlGateway('/cursos/' + id, { method: 'DELETE' });
  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }
  mostrarAlerta(mensajeDelServidor(resultado.datos), 'ok');
  cargarCursos();
}

function limpiarFormularioCurso() {
  document.getElementById('form-curso').reset();
  document.getElementById('curso-id').value = '';
}

/* ---------- ESTUDIANTES ---------- */

async function cargarEstudiantes() {
  const resultado = await pedirAlGateway('/estudiantes');
  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }
  dibujarTablaEstudiantes(resultado.datos);
}

function dibujarTablaEstudiantes(estudiantes) {
  const cuerpo = document.getElementById('tabla-estudiantes');
  if (!estudiantes.length) {
    cuerpo.innerHTML = '<tr><td colspan="6" class="vacio">No hay estudiantes registrados.</td></tr>';
    return;
  }

  cuerpo.innerHTML = estudiantes.map(function (estudiante) {
    return (
      '<tr>' +
      '<td>' + estudiante.id + '</td>' +
      '<td>' + estudiante.cedula + '</td>' +
      '<td>' + estudiante.nombre + '</td>' +
      '<td>' + estudiante.correo + '</td>' +
      '<td>' + estudiante.programa + '</td>' +
      '<td>' +
      '<button type="button" class="boton boton-pequeno" onclick="editarEstudiante(' + estudiante.id + ')">Editar</button>' +
      '<button type="button" class="boton boton-pequeno boton-peligro" onclick="eliminarEstudiante(' + estudiante.id + ')">Eliminar</button>' +
      '</td>' +
      '</tr>'
    );
  }).join('');
}

async function guardarEstudiante(evento) {
  evento.preventDefault();
  const id = document.getElementById('estudiante-id').value;
  const cuerpo = {
    cedula: document.getElementById('estudiante-cedula').value,
    nombre: document.getElementById('estudiante-nombre').value,
    correo: document.getElementById('estudiante-correo').value,
    programa: document.getElementById('estudiante-programa').value
  };

  const ruta = id ? '/estudiantes/' + id : '/estudiantes';
  const resultado = await pedirAlGateway(ruta, {
    method: id ? 'PUT' : 'POST',
    body: cuerpo
  });

  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }

  mostrarAlerta(mensajeDelServidor(resultado.datos), 'ok');
  limpiarFormularioEstudiante();
  cargarEstudiantes();
}

async function editarEstudiante(id) {
  const resultado = await pedirAlGateway('/estudiantes/' + id);
  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }
  const estudiante = resultado.datos;
  document.getElementById('estudiante-id').value = estudiante.id;
  document.getElementById('estudiante-cedula').value = estudiante.cedula;
  document.getElementById('estudiante-nombre').value = estudiante.nombre;
  document.getElementById('estudiante-correo').value = estudiante.correo;
  document.getElementById('estudiante-programa').value = estudiante.programa;
}

async function eliminarEstudiante(id) {
  if (!confirm('¿Eliminar este estudiante?')) {
    return;
  }
  const resultado = await pedirAlGateway('/estudiantes/' + id, { method: 'DELETE' });
  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }
  mostrarAlerta(mensajeDelServidor(resultado.datos), 'ok');
  cargarEstudiantes();
}

function limpiarFormularioEstudiante() {
  document.getElementById('form-estudiante').reset();
  document.getElementById('estudiante-id').value = '';
}

/* ---------- MATRÍCULAS ---------- */

async function cargarMatriculas() {
  const estudiantes = await pedirAlGateway('/estudiantes');
  const cursos = await pedirAlGateway('/cursos');
  const matriculas = await pedirAlGateway('/matriculas');

  if (!estudiantes.ok) {
    mostrarAlerta(mensajeDelServidor(estudiantes.datos), 'error');
    return;
  }
  if (!cursos.ok) {
    mostrarAlerta(mensajeDelServidor(cursos.datos), 'error');
    return;
  }
  if (!matriculas.ok) {
    mostrarAlerta(mensajeDelServidor(matriculas.datos), 'error');
    return;
  }

  llenarSelectEstudiantes(estudiantes.datos);
  llenarSelectCursos(cursos.datos);
  dibujarTablaMatriculas(matriculas.datos, estudiantes.datos, cursos.datos);
}

function llenarSelectEstudiantes(estudiantes) {
  const select = document.getElementById('matricula-estudiante');
  const valorActual = select.value;
  select.innerHTML = textoOpcionVacia('Seleccione un estudiante');
  estudiantes.forEach(function (estudiante) {
    const opcion = document.createElement('option');
    opcion.value = estudiante.id;
    opcion.textContent = estudiante.nombre + ' (ID ' + estudiante.id + ')';
    select.appendChild(opcion);
  });
  if (valorActual) {
    select.value = valorActual;
  }
}

function llenarSelectCursos(cursos) {
  const select = document.getElementById('matricula-curso');
  const valorActual = select.value;
  select.innerHTML = textoOpcionVacia('Seleccione un curso');
  cursos.forEach(function (curso) {
    const opcion = document.createElement('option');
    opcion.value = curso.id;
    opcion.textContent = curso.nombre + ' - ' + curso.codigo;
    select.appendChild(opcion);
  });
  if (valorActual) {
    select.value = valorActual;
  }
}

function dibujarTablaMatriculas(matriculas, estudiantes, cursos) {
  const cuerpo = document.getElementById('tabla-matriculas');
  if (!matriculas.length) {
    cuerpo.innerHTML = '<tr><td colspan="6" class="vacio">No hay matrículas registradas.</td></tr>';
    return;
  }

  cuerpo.innerHTML = matriculas.map(function (matricula) {
    const estudiante = buscarPorId(estudiantes, matricula.estudiante_id);
    const curso = buscarPorId(cursos, matricula.curso_id);
    const nombreEstudiante = estudiante ? estudiante.nombre : 'ID ' + matricula.estudiante_id;
    const nombreCurso = curso ? curso.nombre : 'ID ' + matricula.curso_id;
    return (
      '<tr>' +
      '<td>' + matricula.id + '</td>' +
      '<td>' + nombreEstudiante + '</td>' +
      '<td>' + nombreCurso + '</td>' +
      '<td>' + matricula.anio + '</td>' +
      '<td>' + matricula.periodo + '</td>' +
      '<td>' +
      '<button type="button" class="boton boton-pequeno" onclick="editarMatricula(' + matricula.id + ')">Editar</button>' +
      '<button type="button" class="boton boton-pequeno boton-peligro" onclick="eliminarMatricula(' + matricula.id + ')">Eliminar</button>' +
      '</td>' +
      '</tr>'
    );
  }).join('');
}

async function guardarMatricula(evento) {
  evento.preventDefault();
  const id = document.getElementById('matricula-id').value;
  const cuerpo = {
    estudiante_id: Number(document.getElementById('matricula-estudiante').value),
    curso_id: Number(document.getElementById('matricula-curso').value),
    anio: Number(document.getElementById('matricula-anio').value),
    periodo: document.getElementById('matricula-periodo').value
  };

  const ruta = id ? '/matriculas/' + id : '/matriculas';
  const resultado = await pedirAlGateway(ruta, {
    method: id ? 'PUT' : 'POST',
    body: cuerpo
  });

  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }

  mostrarAlerta(mensajeDelServidor(resultado.datos), 'ok');
  limpiarFormularioMatricula();
  cargarMatriculas();
}

async function editarMatricula(id) {
  const resultado = await pedirAlGateway('/matriculas/' + id);
  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }
  const matricula = resultado.datos;
  document.getElementById('matricula-id').value = matricula.id;
  document.getElementById('matricula-estudiante').value = matricula.estudiante_id;
  document.getElementById('matricula-curso').value = matricula.curso_id;
  document.getElementById('matricula-anio').value = matricula.anio;
  document.getElementById('matricula-periodo').value = matricula.periodo;
}

async function eliminarMatricula(id) {
  if (!confirm('¿Eliminar esta matrícula?')) {
    return;
  }
  const resultado = await pedirAlGateway('/matriculas/' + id, { method: 'DELETE' });
  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }
  mostrarAlerta(mensajeDelServidor(resultado.datos), 'ok');
  cargarMatriculas();
}

function limpiarFormularioMatricula() {
  document.getElementById('form-matricula').reset();
  document.getElementById('matricula-id').value = '';
}

/* ---------- NOTAS ---------- */

async function cargarNotas() {
  const estudiantes = await pedirAlGateway('/estudiantes');
  const cursos = await pedirAlGateway('/cursos');
  const matriculas = await pedirAlGateway('/matriculas');
  const notas = await pedirAlGateway('/notas');

  if (!matriculas.ok) {
    mostrarAlerta(mensajeDelServidor(matriculas.datos), 'error');
    return;
  }
  if (!notas.ok) {
    mostrarAlerta(mensajeDelServidor(notas.datos), 'error');
    return;
  }

  const listaEstudiantes = estudiantes.ok ? estudiantes.datos : [];
  const listaCursos = cursos.ok ? cursos.datos : [];

  llenarSelectMatriculas(matriculas.datos, listaEstudiantes, listaCursos);
  dibujarTablaNotas(notas.datos, matriculas.datos, listaEstudiantes, listaCursos);
}

function textoMatricula(matricula, estudiantes, cursos) {
  const estudiante = buscarPorId(estudiantes, matricula.estudiante_id);
  const curso = buscarPorId(cursos, matricula.curso_id);
  const nombreEstudiante = estudiante ? estudiante.nombre : 'Estudiante ' + matricula.estudiante_id;
  const nombreCurso = curso ? curso.nombre : 'Curso ' + matricula.curso_id;
  return '#' + matricula.id + ' - ' + nombreEstudiante + ' / ' + nombreCurso;
}

function llenarSelectMatriculas(matriculas, estudiantes, cursos) {
  const select = document.getElementById('nota-matricula');
  const valorActual = select.value;
  select.innerHTML = textoOpcionVacia('Seleccione una matrícula');
  matriculas.forEach(function (matricula) {
    const opcion = document.createElement('option');
    opcion.value = matricula.id;
    opcion.textContent = textoMatricula(matricula, estudiantes, cursos);
    select.appendChild(opcion);
  });
  if (valorActual) {
    select.value = valorActual;
  }
}

function dibujarTablaNotas(notas, matriculas, estudiantes, cursos) {
  const cuerpo = document.getElementById('tabla-notas');
  if (!notas.length) {
    cuerpo.innerHTML = '<tr><td colspan="5" class="vacio">No hay notas registradas.</td></tr>';
    return;
  }

  cuerpo.innerHTML = notas.map(function (nota) {
    const matricula = buscarPorId(matriculas, nota.matricula_id);
    const etiqueta = matricula
      ? textoMatricula(matricula, estudiantes, cursos)
      : 'ID ' + nota.matricula_id;
    return (
      '<tr>' +
      '<td>' + nota.id + '</td>' +
      '<td>' + etiqueta + '</td>' +
      '<td>' + nota.calificacion + '</td>' +
      '<td>' + (nota.observacion || '') + '</td>' +
      '<td>' +
      '<button type="button" class="boton boton-pequeno" onclick="editarNota(' + nota.id + ')">Editar</button>' +
      '<button type="button" class="boton boton-pequeno boton-peligro" onclick="eliminarNota(' + nota.id + ')">Eliminar</button>' +
      '</td>' +
      '</tr>'
    );
  }).join('');
}

async function guardarNota(evento) {
  evento.preventDefault();
  const id = document.getElementById('nota-id').value;
  const cuerpo = {
    matricula_id: Number(document.getElementById('nota-matricula').value),
    calificacion: Number(document.getElementById('nota-calificacion').value),
    observacion: document.getElementById('nota-observacion').value
  };

  const ruta = id ? '/notas/' + id : '/notas';
  const resultado = await pedirAlGateway(ruta, {
    method: id ? 'PUT' : 'POST',
    body: cuerpo
  });

  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }

  mostrarAlerta(mensajeDelServidor(resultado.datos), 'ok');
  limpiarFormularioNota();
  cargarNotas();
}

async function editarNota(id) {
  const resultado = await pedirAlGateway('/notas/' + id);
  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }
  const nota = resultado.datos;
  document.getElementById('nota-id').value = nota.id;
  document.getElementById('nota-matricula').value = nota.matricula_id;
  document.getElementById('nota-calificacion').value = nota.calificacion;
  document.getElementById('nota-observacion').value = nota.observacion || '';
}

async function eliminarNota(id) {
  if (!confirm('¿Eliminar esta nota?')) {
    return;
  }
  const resultado = await pedirAlGateway('/notas/' + id, { method: 'DELETE' });
  if (!resultado.ok) {
    mostrarAlerta(mensajeDelServidor(resultado.datos), 'error');
    return;
  }
  mostrarAlerta(mensajeDelServidor(resultado.datos), 'ok');
  cargarNotas();
}

function limpiarFormularioNota() {
  document.getElementById('form-nota').reset();
  document.getElementById('nota-id').value = '';
}
