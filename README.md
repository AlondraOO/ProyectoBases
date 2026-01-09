# ProyectoBases

LINK DE ACCESO: https://proyectobases-r4a6.onrender.com/

NOTA: El servicio de hosting render permite el despliegue durante un numero limitado de minutos, por lo que para su revision, requiere reinicar el deployment

INTRODUCCION:

En este proyecto se desarrolló un modelo de base de datos funcional para un gimnasio, con el propósito de gestionar de forma eficiente la información relacionada con clientes, entrenadores, servicios y pagos. A lo largo del trabajo se presentan las etapas de análisis, diseño e implementación, utilizando distintos tipos de diagramas como Peter Chen, Crow’s Foot y modelo extendido, que permitieron representar de manera clara las relaciones entre las entidades. Finalmente, se diseñó una página web conectada a la base de datos, mostrando su funcionamiento práctico y la integración del modelo propuesto.

El gimnasio Smart Gym necesita llevar un control de la gestión de sus socios, instructores y clases.
De cada socio se desea asignar un ID, almacenar su nombre completo, teléfono, correo electrónico, fecha de inscripción, y tipo de membresía y estado de esta (activa, vencida o pendiente).
De cada instructor se desea guardar el código de instructor, nombre, teléfono, correo electrónico, especialidad y disponibilidad de horarios.
Se desea llevar el control de cada una de las clases que se imparten en el gimnasio. De cada clase se guardará el código de clase, nombre, horario y la capacidad máxima de asistentes.
Un socio puede inscribirse en varias clases, y una clase puede contar con varios socios inscritos; por ello, se registrará la asistencia de cada socio a cada clase con la fecha correspondiente.
Cada clase es impartida por un único instructor, aunque un instructor puede impartir varias clases.
Además, se desea registrar los pagos realizados por los socios. De cada pago se guardará el código de pago (que se incrementará automáticamente), la fecha del pago, el monto y el estado (pagado o pendiente). Un socio puede realizar varios pagos, pero cada pago corresponde únicamente a un socio.
·Entidades: 
- Socio
- Instructor
- Clase
- Asistencia
- Pago

Objetivo del Sistema
 Diseñar una base de datos funcional y una página web que permitan:
Registrar y actualizar socios, instructores, clases y pagos.
Controlar la asistencia de los socios.
Automatizar el estado de membresías.
Generar reportes de asistencia, pagos y clases.


Relaciones Clave
Socio – Inscribe – Clase: un socio puede estar en varias clases; cada clase puede tener varios socios.
Instructor – Imparte – Clase: cada clase tiene un instructor; un instructor puede impartir varias clases.
Socio – Realiza – Pago: un socio puede hacer varios pagos; cada pago pertenece a un solo socio.
Asistencia: registra la participación de socios en clases.
Pago: depende del socio para existir.

INTERFAZ Y VENTANAS

<img width="1800" height="1044" alt="inicio" src="https://github.com/user-attachments/assets/4007f341-47d5-41fb-a663-bee7fef14cfc" />

<img width="1800" height="1049" alt="princip" src="https://github.com/user-attachments/assets/d1923dd9-f1e4-4561-b20e-cd4a0e3c9097" />

<img width="1800" height="1047" alt="socios" src="https://github.com/user-attachments/assets/f92f01ef-ea0b-464f-8ed4-daa02450d47f" />

<img width="1800" height="1045" alt="clases" src="https://github.com/user-attachments/assets/7d37ebfd-d05e-4093-957b-332f4714a0b9" />

<img width="1800" height="1044" alt="instructores" src="https://github.com/user-attachments/assets/a4057b4f-cbb1-4d38-9a42-f0c81346c7ee" />

<img width="1800" height="1046" alt="pagos" src="https://github.com/user-attachments/assets/90cde8a8-d34c-4bcd-8f0c-4221f44a7371" />

<img width="1800" height="1045" alt="asistencia" src="https://github.com/user-attachments/assets/94017569-1035-4a92-98d6-80d8ac594d75" />

<img width="1800" height="1046" alt="nuevo socio" src="https://github.com/user-attachments/assets/1ebef152-3148-4ca2-83eb-d6f9b8101f12" />

<img width="1800" height="1048" alt="nueva clase" src="https://github.com/user-attachments/assets/e18dc774-0f99-43f4-86d1-d967725a23bf" />

