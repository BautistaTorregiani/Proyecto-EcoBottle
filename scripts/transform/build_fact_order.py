import pandas as pd

def transform_fact_order(raw_data, transformed_dims):

    sales_order = raw_data['sales_order']
    
    dim_date = transformed_dims['dim_date']
    dim_channel = transformed_dims['dim_channel']
    dim_customer = transformed_dims['dim_customer']
    dim_store = transformed_dims['dim_store']
    dim_location = transformed_dims['dim_location'] 

    sales_order['order_date_dt'] = pd.to_datetime(sales_order['order_date']).dt.date
    
    for col in ["subtotal", "tax_amount", "shipping_fee", "total_amount"]:
        sales_order[col] = pd.to_numeric(
            sales_order[col].astype(str).str.replace(",", "."),
            errors='coerce'
        ).fillna(0)

    df = sales_order

    # 3. Reemplaza claves de negocio por claves surrogadas
    df = df.merge(dim_date[['date_id', 'date']],
                  left_on='order_date_dt',
                  right_on=pd.to_datetime(dim_date['date']).dt.date,
                  how='left')
    df = df.merge(dim_channel[['channel_sk', 'channel_id']], on='channel_id', how='left')
    df = df.merge(dim_customer[['customer_sk', 'customer_id']], on='customer_id', how='left')
    df = df.merge(dim_store[['store_sk', 'store_id']], on='store_id', how='left')
    
    
    
    # (Shipping)
    df = df.merge(dim_location[['location_sk', 'address_id']],
                  left_on='shipping_address_id',  # Clave del hecho
                  right_on='address_id',          # Clave de la dimensión (BK)
                  how='left')
    df.rename(columns={'location_sk': 'shipping_location_sk'}, inplace=True)
      
    # (Billing)
    df = df.merge(dim_location[['location_sk', 'address_id']],
                  left_on='billing_address_id',   #
                  right_on='address_id',          
                  how='left')
    
 
    df.rename(columns={'location_sk': 'billing_location_sk'}, inplace=True)

    
    cols = [
        "date_id",      
        "channel_sk",
        "store_sk",
        "customer_sk",
        "billing_location_sk",   # La nueva SK de facturación
        "shipping_location_sk",  # La nueva SK de envío
        "status",
        "subtotal",
        "tax_amount",
        "shipping_fee",
        "total_amount"
    ]
    
    fact_order = df[cols].copy()
    
    sk_cols_to_convert = ['date_id', 'channel_sk', 'store_sk', 'customer_sk', 
                          'billing_location_sk', 'shipping_location_sk']
                          
    for col in sk_cols_to_convert:
        if col in fact_order.columns: 
            fact_order[col] = fact_order[col].astype('Int64')

    # Agrega surrogate key incremental 
    fact_order.insert(0, 'order_sk', range(1, len(fact_order) + 1))

    return fact_order