# Introducción al Marketing Online y los Negocios Digitales - TP Final
##  EcoBottle - Desnormalización y Creación de Dashboard

**Alumno:** Torregiani, Bautista  

**Fecha de Entrega:** 17/11/2025
## 1. Introducción y Objetivos
---
El objetivo principal de este proyecto es **diseñar e implementar un mini-ecosistema de datos comercial  y construir un dashboard** que sirva como reporte para un área comercial.

La metodología implementada es el **modelado dimensional (esquema estrella) de Kimball**, asegurando que el modelo de datos esté optimizado para consultas analíticas y reportes.

## 2 Flujo de Datos (ETL)
1.  **Extracción (Extract):** Lee los archivos `.csv` desde el directorio `raw/`.

2.  **Transformación (Transform):** Esta es la fase central donde se aplica el modelado de datos.
    * **Limpieza:** Se limpian y estandarizan los datos (ej. fechas, valores numéricos).
    * **Generación de Dimensiones:** Se crean las tablas de dimensión (ej. `dim_product`, `dim_customer`) y se les asigna una **Clave Surrogada (SK)** única.
    * **Generación de Hechos:** Se construyen las tablas de hechos (ej. `fact_order`). En este paso, se reemplazan las claves de negocio originales (ej. `product_id`) por sus respectivas Claves Surrogadas (SK), creando el modelo estrella final.

3.  **Carga (Load):** Guarda los DataFrames transformados como nuevos archivos `.csv` en el directorio `dw/`.


## 3. Modelo de Datos (Esquema Estrella)
El modelo de datos se descompone 6 esquemas estrella, uno por cada proceso de negocio.

### 3.1. Fact_Order

![Esquema de Ventas (Order)](assets/esquema_fact_order.jpg)

### 3.2. Fact_Order_Item

![Esquema de Detalle de Venta (Order Item)](assets/esquema_fact_order_item.jpg)

### 3.3. Fact_Shipment

![Esquema de Envíos (Shipment)](assets/esquema_fact_shipment.jpg)

### 3.4. Fact_Nps_Response

![Esquema de Encuestas (NPS)](assets/esquema_fact_nps_response.jpg)

### 3.5. Fact_Web_Session

![Esquema de Actividad Web (Web Session)](assets/esquema_fact_web_session.jpg)


### 3.6. Fact_Payment

![Esquema de Pagos (Payment)](assets/esquema_fact_payment.jpg)


## 📊 Dashboard en Power BI

El dashboard interactivo con todos los KPIs del proyecto se puede consultar en el siguiente enlace:

**[Acceso al Dashboard](https://app.powerbi.com/groups/b750b959-b95e-476b-9a28-42cc455b124d/reports/50382176-c6dc-411c-a5b6-d86b6c34b489/1340d953aaf8568da55a?experience=power-bi)**


![Captura del Dashboard](assets/dashboard.png)

## 4. ⚙️ Instrucciones de Ejecución
Se deben de seguir estos pasos para replicar el entorno y procesar los datos.

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/BautistaTorregiani/mkt_tp_final.git](https://github.com/BautistaTorregiani/mkt_tp_final.git)
    cd mkt_tp_final
    ```

2.  **Crear y activar el entorno virtual**:
    ```bash
    # En Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # En macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    El archivo `requirements.txt` contiene todas las librerías de Python necesarias.
    ```bash
    pip install -r requirements.txt
    ```

4. **Ejecución del Proceso ETL:**

    El script `main.py` actúa como orquestador central y maneja todo el proceso ETL. Este script se encarga de ejecutar las transformaciones en el orden correct para asegurar la integridad.

    Para ejecutar el pipeline completo, se debe ejecutar:

    ```bash
    python main.py



## 5. 📘 Diccionario de Datos
El presente Diccionario de Datos detalla los campos, tipos de datos y descripciones de cada tabla que conforma el modelo estrella del proyecto.
Su propósito es documentar la estructura del Data Warehouse, facilitando la comprensión de las dimensiones y hechos.
### Dimensiones (Dims):
---
### Dim_Product
| Campo           | Tipo de dato  | Descripción                            |
| --------------- | ------------- | -------------------------------------- |
| `product_sk`    | INT           | Clave sustituta (PK).                  |
| `product_id`    | INT           | Identificador original del producto.   |
| `product_name`  | VARCHAR(120)  | Nombre del producto.                   |
| `sku`           | VARCHAR(40)   | Código único de producto (Unique).     |
| `category_name` | VARCHAR(80)   | Categoría del producto.                |
| `list_price`    | DECIMAL(12,2) | Precio de lista.                       |
| `status`        | CHAR(1)     | Estado del producto (activo/inactivo). |
***
### Dim_Channel
| Campo          | Tipo de dato | Descripción                              |
| -------------- | ------------ | ---------------------------------------- |
| `channel_sk`   | INT          | Clave sustituta (PK).                    |
| `channel_id`   | INT          | Identificador original del canal.        |
| `channel_name` | VARCHAR(20)  | Nombre del canal (Online, Tienda, etc.). |
| `channel_code` | VARCHAR(50)  | Código único del canal (Unique).         |
***
### Dim_Customer
| Campo         | Tipo de dato | Descripción                                |
| ------------- | ------------ | ------------------------------------------ |
| `customer_sk` | INT          | Clave sustituta (PK).                      |
| `customer_id` | INT          | Identificador original del cliente.        |
| `email`       | VARCHAR(120) | Correo electrónico del cliente.            |
| `first_name`  | VARCHAR(80)  | Nombre del cliente.                        |
| `last_name`   | VARCHAR(80)  | Apellido del cliente.                      |
| `status`      | CHAR(1)      | Estado del cliente (A=Activo, I=Inactivo). |
| `phone`       | VARCHAR(255) | Teléfono (opcional).                       |
| `created_at`  | TIMESTAMP    | Fecha de creación del registro.            |

***
### Dim_Date
| Campo              | Tipo de dato | Descripción                  |
| ------------------ | ------------ | ---------------------------- |
| `date_id`          | INT          | Clave sustituta (PK).        |
| `date`             | DATE         | Fecha completa (YYYY-MM-DD). |
| `year`             | SMALLINT     | Año.                         |
| `month`            | SMALLINT     | Mes numérico.                |
| `month_name`       | VARCHAR(20)  | Nombre del mes.              |
| `day`              | SMALLINT     | Día del mes.                 |
| `quarter`          | SMALLINT     | Trimestre.                   |
| `day_of_week_name` | VARCHAR(20)  | Día de la semana.            |

***

### Dim_Location
| Campo           | Tipo de dato | Descripción                          |
| --------------- | ------------ | ------------------------------------ |
| `location_sk`   | INT          | Clave sustituta (PK).                |
| `address_id`    | INT          | Identificador de dirección original. |
| `line1`         | VARCHAR(120) | Dirección principal.                 |
| `line2`         | VARCHAR(120) | Dirección secundaria (opcional).     |
| `city`          | VARCHAR(255) | Ciudad.                              |
| `postal_code`   | VARCHAR(20)  | Código postal.                       |
| `province_name` | VARCHAR(50)  | Provincia o estado.                  |
| `province_code` | VARCHAR(10)  | Código de provincia.                 |
| `country_code`  | CHAR(2)    | Código de país.                      |
***
### Dim_Store
| Campo           | Tipo de dato | Descripción                          |
| --------------- | ------------ | ------------------------------------ |
| `store_sk`      | INT          | Clave sustituta (PK).                |
| `store_id`      | INT          | Identificador original de la tienda. |
| `store_name`    | VARCHAR(80)  | Nombre de la tienda.                 |
| `line1`         | VARCHAR(120) | Dirección principal.                 |
| `line2`         | VARCHAR(120) | Dirección secundaria.                |
| `city`          | VARCHAR(80)  | Ciudad.                              |
| `postal_code`   | VARCHAR(20)  | Código postal.                       |
| `province_name` | VARCHAR(50)  | Provincia.                           |
| `province_code` | VARCHAR(10)  | Código de provincia.                 |
| `country_code`  | CHAR(2)      | Código de país.                      |
| `created_at`    | TIMESTAMP    | Fecha de creación del registro.      |
---
### Hechos (Facts):
---
### Fact_Order
| Campo                  | Tipo de dato | Descripción                                     |
| ---------------------- | ------------ | ----------------------------------------------- |
| `order_sk`             | INT          | Clave sustituta (PK).                           |
| `date_id`              | INT          | FK → `Dim_Date(date_id)`. Fecha del pedido.     |
| `channel_sk`           | INT          | FK → `Dim_Channel(channel_sk)`.                 |
| `store_sk`             | INT          | FK → `Dim_Store(store_sk)`.                     |
| `customer_sk`          | INT          | FK → `Dim_Customer(customer_sk)`.               |
| `billing_location_sk`  | INT          | FK → `Dim_Location(location_sk)`                |
| `shipping_location_sk` | INT          | FK → `Dim_Location(location_sk)`                |
| `status`               | VARCHAR(20)  | Estado del pedido.                              |
| `subtotal`             | DECIMAL(12,2) | Subtotal de la venta.                          |
| `tax_amount`           | DECIMAL(12,2) | Monto de impuestos.                            |
| `shipping_fee`         | DECIMAL(12,2) | Costo de envío.                                |
| `total_amount`         | DECIMAL(12,2) | Total del pedido.                              |
---
### Fact_Order_Item
| Campo             | Tipo de dato | Descripción                                        |
| ----------------- | ------------ | -------------------------------------------------- |
| `order_item_sk`   | INT          | Clave sustituta (PK).                              |
| `date_id`         | INT          | FK → `Dim_Date(date_id)`.                          |
| `channel_sk`      | INT          | FK → `Dim_Channel(channel_sk)`.                    |
| `store_sk`        | INT          | FK → `Dim_Store(store_sk)`.                        |
| `customer_sk`     | INT          | FK → `Dim_Customer(customer_sk)`.                  |
| `location_sk`     | INT          | FK → `Dim_Location(location_sk)`.                  |
| `product_sk`      | INT          | FK → `Dim_Product(product_sk)`.                    |
| `quantity`        | INT          | Cantidad vendida.                                  |
| `unit_price`      | DECIMAL(12,2) | Precio unitario.                                   |
| `discount_amount` | DECIMAL(12,2) | Descuento aplicado.                                |
| `line_total`      | DECIMAL(12,2) | Total de la línea (cantidad × precio – descuento). |
---
### Fact_Payment
| Campo             | Tipo de dato | Descripción                                    |
| ----------------- | ------------ | ---------------------------------------------- |
| `payment_sk`      | INT          | Clave sustituta (PK).                          |
| `paid_at_date_id` | INT          | FK → `Dim_Date(date_id)`.                      |
| `paid_at_time`    | TIME         | Hora del pago.                                 |
| `customer_sk`     | INT          | FK → `Dim_Customer(customer_sk)`.              |
| `channel_sk`      | INT          | FK → `Dim_Channel(channel_sk)`.                |
| `store_sk`        | INT          | FK → `Dim_Store(store_sk)`.                    |
| `location_sk`     | INT          | FK → `Dim_Location(location_sk)`.              |
| `status`          | VARCHAR(20)  | Estado del pago.                               |
| `method`          | VARCHAR(255) | Método de pago (tarjeta, transferencia, etc.). |
| `transaction_ref` | VARCHAR(255) | Código o referencia de transacción.            |
| `amount`          | DECIMAL(12,2) | Monto abonado.                                 |
---
### Fact_Shipment
| Campo               | Tipo de dato | Descripción                                  |
| ------------------- | ------------ | -------------------------------------------- |
| `shipment_sk`       | INT          | Clave sustituta (PK).                        |
| `shipped_date_id`   | INT          | FK → `Dim_Date(date_id)` (fecha de envío).   |
| `shipped_at_time`   | TIME         | Hora de envío.                               |
| `delivered_date_id` | INT          | FK → `Dim_Date(date_id)` (fecha de entrega). |
| `delivered_at_time` | TIME         | Hora de entrega.                             |
| `customer_sk`       | INT          | FK → `Dim_Customer(customer_sk)`.            |
| `channel_sk`        | INT          | FK → `Dim_Channel(channel_sk)`.              |
| `store_sk`          | INT          | FK → `Dim_Store(store_sk)`.                  |
| `location_sk`       | INT          | FK → `Dim_Location(location_sk)`.            |
| `carrier`           | VARCHAR(40)  | Empresa de transporte.                       |
| `tracking_number`   | VARCHAR(60)  | Número de seguimiento del envío.             |
---
### Fact_Nps_Response
| Campo                  | Tipo de dato | Descripción                                 |
| ---------------------- | ------------ | ------------------------------------------- |
| `nps_response_sk`      | INT          | Clave sustituta (PK).                       |
| `responded_at_date_id` | INT          | FK → `Dim_Date(date_id)` (fecha respuesta). |
| `responded_at_time`    | TIME         | Hora de respuesta.                          |
| `customer_sk`          | INT          | FK → `Dim_Customer(customer_sk)`.           |
| `channel_sk`           | INT          | FK → `Dim_Channel(channel_sk)`.             |
| `score`                | SMALLINT     | Puntaje NPS (0 a 10).                       |
| `comment`              | TEXT         | Comentario del cliente (opcional).          |
---
### Fact_Web_Session
| Campo             | Tipo de dato | Descripción                                      |
| ----------------- | ------------ | ------------------------------------------------ |
| `session_sk`      | INT          | Clave sustituta (PK).                            |
| `started_date_id` | INT          | FK → `Dim_Date(date_id)` (inicio).               |
| `started_at_time` | TIME         | Hora de inicio.                                  |
| `ended_date_id`   | INT          | FK → `Dim_Date(date_id)` (fin).                  |
| `ended_at_time`   | TIME         | Hora de finalización.                            |
| `customer_sk`     | INT          | FK → `Dim_Customer(customer_sk)`.                |
| `source`          | VARCHAR(50)  | Fuente de tráfico (Google, Direct, Email, etc.). |
| `device`          | VARCHAR(30)  | Dispositivo utilizado (mobile, desktop, tablet). |


---
## 6. Supuestos y Decisiones de Modelado

Durante el desarrollo del proyecto, se tomaron las siguientes decisiones clave:

1.  **Claves Surrogadas (SK) vs. Claves de Negocio (BK):**
    * Todas las dimensiones utilizan una **SK** (ej: `product_sk`) autoincremental como Clave Primaria (PK). Esto asegura la integridad referencial y desacopla el DW de los sistemas de producción, esto significa que las conexiones entre tus tablas (como 'Ventas' y 'Productos') nunca se rompen y que el dashboard no se daña si los IDs del sistema original cambian.
    * Las **BK** (ej: `product_id`) se conservan en la dimensión para permitir el *lookup* (búsqueda) durante el proceso ETL.


## 7. Consultas Clave

Las siguientes medidas DAX fueron creadas en Power BI para implementar la lógica de negocio y calcular los KPIs principales solicitados.

### Total Ventas ($M)
Esta medida calcula la suma de `total_amount` únicamente para las órdenes consideradas "válidas" (pagadas o completadas).

```dax
Total Ventas = 
CALCULATE(
    SUM(Fact_Order[total_amount]),
    Fact_Order[status] IN {"PAID", "FULFILLED"}
)
```
---
### Ticket Promedio ($K)
Esta medida calcula el promedio de total_amount utilizando el mismo filtro de "ventas válidas" que el KPI anterior

```dax
Ticket Promedio = 
CALCULATE(
    AVERAGE(Fact_Order[total_amount]),
    Fact_Order[status] IN {"PAID", "FULFILLED"}
)
```
---
### Usuarios Activos
Calcula el conteo único de clientes que tuvieron al menos una sesión web.

```dax
Usuarios Activos = 
DISTINCTCOUNT('fact_web_session'[customer_sk])
```
---
### NPS
El NPS (Net Promoter Score) se calcula midiendo la proporción de clientes promotores y detractores.
Primero, se obtiene el porcentaje de promotores, es decir, los clientes que calificaron con 9 o 10 puntos, y el porcentaje de detractores, que son los que calificaron entre 0 y 6 puntos.
Luego, la fórmula final es:

(Porcentaje de Promotores − Porcentaje de Detractores) × 100
```dax
NPS = 
VAR TotalRespuestas =
    COUNT ( 'fact_nps_response'[score] )
VAR Promotores =
    CALCULATE (
        COUNT ( 'fact_nps_response'[score] ),
        'fact_nps_response'[score] >= 9
    )
VAR Detractores =
    CALCULATE (
        COUNT ( 'fact_nps_response'[score] ),
        'fact_nps_response'[score] <= 6
    )
RETURN
    DIVIDE ( ( Promotores - Detractores ), TotalRespuestas ) * 100
```