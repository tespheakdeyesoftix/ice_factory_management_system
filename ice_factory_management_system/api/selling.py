import frappe 
@frappe.whitelist()
def get_dashboard_data(outlet, date):
    # outlet, date
    sql = """select 
            count(*) as total_order, 
            sum(total_sale_quantity) as total_quantity, 
            sum(total_amount) as total_amount 
        from `tabSale` 
    where 
    sale_status = 'Closed' and 
    posting_date = %(date)s and 
    outlet = %(outlet)s 
    """
    data = frappe.db.sql(sql,{"outlet":outlet, "date":date},as_dict = 1)
 
    if data: 
        return data[0]
    
    return {
        "total_order":0,
        "total_quantity":0,
        "total_amount": 0
    }

@frappe.whitelist()
def get_total_daily_sale_product_summary(outlet="", start_date=None,end_date=None,customer=""):
    if not start_date:
        start_date = frappe.utils.today()
        
    if not end_date:
        end_date = frappe.utils.today()

    # outlet, date
    sql = """select 
            coalesce(sp.photo,'') as photo,
            sp.unit,
            sp.product_code,
            sp.product_name,
            sp.allow_sum_qty,
            sum(sp.quantity) as quantity, 
            sum(sp.free_quantity) as free_quantity, 
            sum(sp.return_quantity) as return_quantity, 
            sum(coalesce(sp.total_sale_quantity,0)) as sale_quantity, 
            sum(sp.total_amount) as total_amount 
            
        from `tabSale Products` sp
        inner join `tabSale` s on s.name = sp.parent 

    where 
        s.sale_status = 'Closed' and 
        s.posting_date between %(start_date)s and %(end_date)s and 
        (%(outlet)s = '' or s.outlet = %(outlet)s)   and 
        (%(customer)s = '' or s.customer = %(customer)s)
    group by
         coalesce(sp.photo,'') ,
        sp.product_code,
        sp.product_name,
        sp.unit,
        sp.allow_sum_qty
    """ 
    

    data = frappe.db.sql(sql,{"outlet":outlet, "start_date":start_date, "end_date":end_date,"customer":customer},as_dict = 1)
    return data

@frappe.whitelist()
def add_audit_trails(sale,data):
    for d in data:
        doc =  frappe.get_doc(d)
        doc.ref_doc_name = sale,
        doc.username = frappe.session.user.split("@")[0]
        doc.insert(ignore_permissions=True)
    frappe.db.commit()


@frappe.whitelist()
def get_split_bill_list(name):
    sql="""
        select 
            name,customer,customer_name,
            reference_number,
            customer_photo,
            phone_number,
            can_show_price,
            status,
            total_sale_quantity,
            total_amount,
            owner,
            creation
        from `tabSale` 
        where
            parent_bill_number = %(name)s and 
            sale_status <> 'Deleted'
        order by 
            name
    """

    data = frappe.db.sql(sql,{"name":name},as_dict = 1)

    sql = """
        select 
            parent,
            product_code,
            product_name,
            total_sale_quantity,
            total_amount,
            price,
            unit
        from `tabSale Products` 
        where 
            parent in %(names)s
    """
    data_product = []
    if data:
        data_product = frappe.db.sql(sql,{"names":[d.get("name") for d in data]},as_dict = 1)

    for d in data:
        d["sale_products"] = [sp for sp in data_product if sp.get("parent")==d.get("name")]

    return data


@frappe.whitelist()
def search(keyword=""):
    if not keyword:
        frappe.throw("សូមបញ្ជូលពាក្យត្រូវស្វែងរក")
    if len(keyword)<2:
        frappe.throw("សូមបញ្ជូលពាក្យត្រូវស្វែងរកយ៉ាងតិចចំនួនពីរពាក្យ")
    meta = frappe.get_meta("Sale")
    
    filters = [["name","like",f"%{keyword.strip()}%"]]
    if meta.search_fields:
        search_fields = meta.search_fields.split(",")

        for f in search_fields:
            if not next((r for r in meta.fields if r.get("fieldname") == f ), None).get("fieldtype") in ["Date","DateTime","Datetime"]:
                filters.append([f.strip(),"like",f"%{keyword}%"])
    
    fields = ["name","owner","modified","status","sale_status","customer","customer_name","customer_photo","total_amount"]
    data = frappe.db.get_list("Sale",fields=fields, or_filters=filters,page_length=20, order_by='posting_date desc',)
    if not data:
        frappe.throw("មិនមានលទ្ធផលត្រូវនឹងលក្ខខណ្ឌស្វែងរករបស់អ្នកទេ")
    return data
    