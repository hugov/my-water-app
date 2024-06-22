CREATE TABLE public.produto (
	id serial NOT NULL,
	nome varchar NULL,
	descricao varchar NULL,
	preco decimal NULL,
	status decimal NULL,
	data_criacao date NULL,
	CONSTRAINT produto_pk PRIMARY KEY (id)
);

COMMENT ON COLUMN public.produto.id IS 'Identificador único do produto';
COMMENT ON COLUMN public.produto.nome IS 'Nome do produto';
COMMENT ON COLUMN public.produto.descricao IS 'Descrição detalhada do produto';
COMMENT ON COLUMN public.produto.preco IS 'Preço unitário do produto';
COMMENT ON COLUMN public.produto.status IS 'Situação do cadastro do produto.
1 - Ativo
0 - Inativo';
COMMENT ON COLUMN public.produto.data_criacao IS 'Data de criação do produto';
