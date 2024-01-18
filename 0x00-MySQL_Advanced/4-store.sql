-- creates a trigger that decreases the quantity of an item after adding a new order.
DELIMITER //
CREATE TRIGGER first_table
AFTER INSERT ON `orders`
FOR EACH ROW
BEGIN
    IF EXISTS ( SELECT * FROM items WHERE items.name = NEW.item_name) THEN
        UPDATE items
        SET quantity = quantity - NEW.number
        WHERE items.name = NEW.item_name;
    END IF;
END;
//
DELIMITER ;
