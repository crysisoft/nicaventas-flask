
CREATE TABLE "public"."actives" (
  "id" serial,
  "city" varchar(128) COLLATE "pg_catalog"."default",
  "country" varchar(60) COLLATE "pg_catalog"."default" NOT NULL,
  "active" bool,  
  CONSTRAINT "actives_pkey" PRIMARY KEY ("id")
);

CREATE TABLE "public"."descripciones" (
  "id" serial,
  "sku" varchar(7) COLLATE "pg_catalog"."default" NOT NULL,
  "descripcion" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "precio" float8 NOT NULL,
  CONSTRAINT "descripciones_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "descripciones_sku_key" UNIQUE ("sku")
);

CREATE TABLE "public"."reglas" (
  "id_regla" serial,
  "country" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "city" varchar(60) COLLATE "pg_catalog"."default" NOT NULL,
  "sku" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "min_condition" int4 NOT NULL,
  "max_condition" int4 NOT NULL,
  "variation" float8 NOT NULL,
  CONSTRAINT "reglas_pkey" PRIMARY KEY ("id_regla"),
  CONSTRAINT "reglas_sku_fkey" FOREIGN KEY ("sku") REFERENCES "public"."descripciones" ("sku") ON DELETE NO ACTION ON UPDATE NO ACTION
);

INSERT INTO "public"."actives"("city", "active", "country") VALUES ('Nueva Guinea', 't', 'ni');
INSERT INTO "public"."actives"("city", "active", "country") VALUES ('Masaya', 't', 'ni');
INSERT INTO "public"."actives"("city", "active", "country") VALUES ('Esteli', 't', 'ni');
INSERT INTO "public"."actives"("city", "active", "country") VALUES ('León', 't', 'ni');
INSERT INTO "public"."actives"("city", "active", "country") VALUES ('Chinandega', 't', 'ni');
INSERT INTO "public"."actives"("city", "active", "country") VALUES ('Matagalpa', 't', 'ni');
INSERT INTO "public"."actives"("city", "active", "country") VALUES ('Managua', 't', 'ni');
INSERT INTO "public"."actives"("city", "active", "country") VALUES ('Granada', 't', 'ni');


INSERT INTO "public"."descripciones"("sku", "descripcion", "precio") VALUES ('AZ00001', 'Paraguas de señora estampado', 10);
INSERT INTO "public"."descripciones"("sku", "descripcion", "precio") VALUES ('AZ00002', 'Helado de sabor fresa', 1);
INSERT INTO "public"."descripciones"("sku", "descripcion", "precio") VALUES ('AZ00003', 'Sandalia para caballero', 15);
INSERT INTO "public"."descripciones"("sku", "descripcion", "precio") VALUES ('AZ00004', 'Mochila', 12);

INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Esteli', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Esteli', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Esteli', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Esteli', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'El Rama', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'El Rama', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'El Rama', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'El Rama', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'León', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'León', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'León', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'León', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00001', 800, 810, 0.5);
