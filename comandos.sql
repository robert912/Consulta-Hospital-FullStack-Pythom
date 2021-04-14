
create database hospital;
create table consulta(id_consulta int not null,tipo_consulta varchar(50), num_pacientes_atendido int, nombre_especialista varchar(50), estado boolean, primary key (id_consulta));
create table paciente(id_paciente int auto_increment not null, nombre varchar(50), edad int, historia_clinica float, id_consulta int, primary key (id_paciente), foreign key (id_consulta) references consulta(id_consulta));


insert into consulta values(1, "Pediatria", 0, "Daniela Bustamante", true);
insert into consulta values(2, "Urgencia", 0, "Vincent DeVita", true);
insert into consulta values(3, "CGI", 0, "Alexander Fleming", true);
select * from consulta;

insert into paciente  values(1, "Roberto Orellana", 31, 3, 3);
insert into paciente  values(2, "Kimberly Orellana", 14, 3, 1);
insert into paciente  values(3, "Rosa Tamayo", 60, 5, 2);
insert into paciente  values(4, "Juan Perez", 27, 5, 2);
insert into paciente  values(5, "Pedro Picasso", 18, 4, 3);
insert into paciente  values(6, "Larry Page", 41, 5, 2);
select * from paciente;

Select * from paciente order by historia_clinica desc;
Select *, (edad*historia_clinica)/100 as Riesgo from paciente order by historia_clinica desc;
Select * from paciente where id_consulta = 2 and edad >=16 and edad <=40 order by historia_clinica desc;
select * from paciente where edad = (Select max(edad) from paciente);
select * from consulta where num_pacientes_atendido = (Select max(num_pacientes_atendido) from consulta);

