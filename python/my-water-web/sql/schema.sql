CREATE TABLE public.produto (
	id serial NOT NULL,
	name varchar NULL,
	description varchar NULL,
	price decimal NULL,
	status decimal NULL,
	creation_date date NULL,
	CONSTRAINT produto_pk PRIMARY KEY (id)
);

COMMENT ON COLUMN public.produto.id IS 'Identificador único do produto';
COMMENT ON COLUMN public.produto.name IS 'Nome do produto';
COMMENT ON COLUMN public.produto.description IS 'Descrição detalhada do produto';
COMMENT ON COLUMN public.produto.price IS 'Preço unitário do produto';
COMMENT ON COLUMN public.produto.status IS 'Situação do cadastro do produto.
1 - Ativo
0 - Inativo';
COMMENT ON COLUMN public.produto.creation_date IS 'Data de criação do produto';
