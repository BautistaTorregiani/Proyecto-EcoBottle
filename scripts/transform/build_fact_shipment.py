import pandas as pd

def transform_fact_shipment(raw_data, transformed_dims, fact_order):
    shipment = raw_data['shipment']
    sales_order = raw_data['sales_order']
    
    dim_date = transformed_dims['dim_date']
    dim_customer = transformed_dims['dim_customer']
    dim_channel = transformed_dims['dim_channel']
    dim_store = transformed_dims['dim_store']
    dim_location = transformed_dims['dim_location']

 # --- Traigo datos de la orden por BK (order_id)
    df = shipment.merge(
    sales_order[['order_id','customer_id','channel_id','store_id','shipping_address_id']],
    on="order_id", how="left"
)

# --- 🔹 Un único merge con fact_order para traer order_sk (y date_id si lo querés)
    df = df.merge(
    fact_order[['order_id', 'order_sk', 'date_id']],
    on='order_id',
    how='left'
)


    # Claves foráneas
    df = df.merge(dim_customer[['customer_sk', 'customer_id']], on='customer_id', how='left')
    df = df.merge(dim_channel[['channel_sk', 'channel_id']], on='channel_id', how='left')
    df = df.merge(dim_store[['store_sk', 'store_id']], on='store_id', how='left')
    df = df.merge(
        dim_location[['location_sk', 'address_id']],
        left_on='shipping_address_id',
        right_on='address_id',
        how='left'
    )

    # Fechas
    df['shipped_at'] = pd.to_datetime(df['shipped_at'], errors='coerce')
    df['delivered_at'] = pd.to_datetime(df['delivered_at'], errors='coerce')

    df['shipped_at_dt'] = df['shipped_at'].dt.date
    df['shipped_at_time'] = df['shipped_at'].dt.time
    df['delivered_at_dt'] = df['delivered_at'].dt.date
    df['delivered_at_time'] = df['delivered_at'].dt.time

    dim_date_shipped = dim_date.rename(columns={'date_id': 'shipped_date_id', 'date': 'shipped_date'})
    dim_date_delivered = dim_date.rename(columns={'date_id': 'delivered_date_id', 'date': 'delivered_date'})

    df = df.merge(
        dim_date_shipped[['shipped_date_id', 'shipped_date']],
        left_on='shipped_at_dt',
        right_on=pd.to_datetime(dim_date_shipped['shipped_date']).dt.date,
        how='left'
    )
    df = df.merge(
        dim_date_delivered[['delivered_date_id', 'delivered_date']],
        left_on='delivered_at_dt',
        right_on=pd.to_datetime(dim_date_delivered['delivered_date']).dt.date,
        how='left'
    )

    # 🔹 Columnas finales (incluye order_sk)
    cols = [
        "shipment_sk",
        "order_sk", #Añadi esta dimensio degenerada para poder obtener mayor informacion para uso en dashboard.
        "shipped_date_id",
        "shipped_at_time",
        "delivered_date_id",
        "delivered_at_time",
        "customer_sk",
        "channel_sk",
        "store_sk",
        "location_sk",
        "carrier",
        "tracking_number"
    ]

    fact_shipment = df.copy()
    fact_shipment.insert(0, 'shipment_sk', range(1, len(fact_shipment) + 1))
    fact_shipment = fact_shipment[cols]

    # Tipos
    fact_shipment['shipped_date_id'] = fact_shipment['shipped_date_id'].astype('Int64')
    fact_shipment['delivered_date_id'] = fact_shipment['delivered_date_id'].astype('Int64')
    fact_shipment['order_sk'] = fact_shipment['order_sk'].astype('Int64')

    return fact_shipment
