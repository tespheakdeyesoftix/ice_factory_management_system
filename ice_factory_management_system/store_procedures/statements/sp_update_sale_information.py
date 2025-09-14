SQL = """CREATE PROCEDURE `sp_update_sale_information`(IN `v_sale` varchar(100),IN `v_sale_payment` varchar(100))
BEGIN
	create temporary table if not exists tbl_sale(name varchar(50));
    
	if v_sale <>'' then
		update `tabSale` s
		LEFT JOIN (
			select 
				sale,
				sum(payment_amount) as payment_amount,
				sum(write_off_amount) as write_off_amount
			from `tabSale Payment Invoices` 
			WHERE
				parenttype = 'Sale Payment' and 
				sale = v_sale and 
				docstatus = 1
			group by sale
		) b on b.sale = s.name
		SET	
			s.total_payment = COALESCE(b.payment_amount,0),
			s.total_write_off = coalesce(b.write_off_amount,0),
			s.balance = s.total_amount - (coalesce(b.payment_amount,0) + COALESCE(b.write_off_amount,0)),
			s.status = fn_get_payment_status(s.total_amount,(coalesce(b.payment_amount,0) + COALESCE(b.write_off_amount,0)) )
		WHERE
			s.name = v_sale;
			
			
	end if;
	 
	
	-- if user pass sale payment name then update all sale in sale payment invoice
		if v_sale_payment <>'' then
        
        -- get sale invoice from sale payment invoice add to temp data
        insert into tbl_sale select sale from `tabSale Payment Invoices` where parent = v_sale_payment;
        
		update `tabSale` s
		LEFT JOIN (
			select 
				sale,
				sum(payment_amount) as payment_amount,
				sum(write_off_amount) as write_off_amount
			from `tabSale Payment Invoices` 
			WHERE
				sale in (select name from tbl_sale) and
				docstatus = 1
			group by sale
		) b on b.sale = s.name
		SET	
			s.total_payment = coalesce(b.payment_amount,0),
			s.total_write_off =coalesce( b.write_off_amount,0),
			s.balance = coalesce(s.total_amount,0) - (coalesce(b.payment_amount,0) + COALESCE(b.write_off_amount,0)),
			s.status = fn_get_payment_status(s.total_amount,(coalesce(b.payment_amount,0) + COALESCE(b.write_off_amount,0)) )
		WHERE
			s.name in (select name from tbl_sale);
		
	end if;
	
	 

END"""