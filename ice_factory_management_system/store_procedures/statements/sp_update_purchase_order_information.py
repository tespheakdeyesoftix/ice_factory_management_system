SQL = """CREATE PROCEDURE `sp_update_purchase_order_information`(IN `v_purchase_order` varchar(100),IN `v_purchase_order_payment` varchar(100))
BEGIN
	create temporary table if not exists temp_purchase_order(name varchar(50));
    
	IF v_purchase_order <>'' THEN
		update `tabPurchase Order` s
		LEFT JOIN (
			select 
				purchase_order,
				sum(payment_amount) as payment_amount,
				sum(write_off_amount) as write_off_amount
			from `tabPurchase Order Payment Invoices` 
			WHERE 1 = 1
				and parenttype = 'Purchase Order Payment' 
				and purchase_order = v_purchase_order 
				and docstatus = 1
			group by 
            	purchase_order
		) b on b.purchase_order = s.name
		SET	
			s.total_cost = COALESCE(b.payment_amount,0),
			s.total_write_off = coalesce(b.write_off_amount,0),
			s.balance = s.total_cost - (coalesce(b.payment_amount,0) + COALESCE(b.write_off_amount,0))
		WHERE
			s.name = v_purchase_order;
            			
	END IF;
	 
	
	-- if user pass purchase-order payment name then update all purchase-orders in purchase-order payment invoice
	IF v_purchase_order_payment <>'' THEN        
        -- get purchase-order invoice from purchase-order payment invoice add to temp data
        
        insert into temp_purchase_order select purchase_order from `tabPurchase Order Payment Invoices` where parent = v_purchase_order_payment;        
		update `tabPurchase Order` s
		LEFT JOIN (
			select 
				purchase_order,
				sum(payment_amount) as payment_amount,
				sum(write_off_amount) as write_off_amount
			from `tabPurchase Order Payment Invoices` 
			WHERE 1 = 1
				and purchase_order in (select name from temp_purchase_order)
				and docstatus = 1
			group by 
            	purchase_order
		) b on b.purchase_order = s.name
		SET	
			s.total_payment = coalesce(b.payment_amount,0),
			s.total_write_off =coalesce( b.write_off_amount,0),
			s.balance = coalesce(s.total_cost,0) - (coalesce(b.payment_amount,0) + COALESCE(b.write_off_amount,0))
		WHERE
			s.name in (select name from temp_purchase_order);
		
	END IF; 
END"""