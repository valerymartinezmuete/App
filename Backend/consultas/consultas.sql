
-- Consulta para ingresos
select
	"Fecha",
	"Empresa",
	"Saldo",
	"Tercero"
from public."Movimientos"
where
	"Fecha" >= '2026-01-01'
	and "Empresa" in ('RBG CONSULTING SAS BIC', 'RBG LEGAL SAS BIC', 'Russell Bedford', 'ARA')
	and "Cod_Clase" = '4';

-- Consulta para cartera abierta
select
	"Empresa",
	"Unidad de Negocio",
	"Tercero",
	"Tipo Documento",
	"Número Documento",
	"Fecha",
	"Fecha Vencimiento",
	"Edad",
	"Mora"
	"Saldo",
	nombre_vendedor
from public."Cartera Abierta"
where
	"Empresa" in ('RBG CONSULTING SAS BIC', 'RBG LEGAL SAS BIC', 'RUSSELL BEDFORD RBG S.A.S. BIC', 'ARA CONSULTING SAS')
	and "Edad" in ('Ven. 181 a 360', 'Ven. 361 a 720', 'Ven. 61 a 90', 'Ven. 721 a 9999', 'Ven. 91 a 180')
	and "Tipo Documento" = 'FEV'
	;