
Important: to make use of this API program , all your items need to have an SKU that matches the Barcode on the item.
The programm can be controlled just with a simple barcode scanner, no Keyboard or mouse needed.

Setup:
To log in you, will need to enter your smander credentials into the program before running it.
you find these variable at the top of the file.
2 special Barcodes are provided (NO, YES)

Run warehouse in the linux terminal (for example on a single board computer) with "python3 warehouse.py"
this also works over ssh.
the programm now authenticates with the Smander.com Server
It will next download a json file with the orders that are currently in the stage "processing" in your store.
That means payment for these orders has been processed and they are ready to be packed.

Warehouse now lists all the open Orders.
Scan any barcode to continue. or press Enter if there is a keyboard connected.

It will then list the first item of the first order and ask you to scan it.
If the scan enters the expected SKU/EAN it will directly proced to the next item on thelist.

if the item is not available at the moment you can cancel it and go to the next line by scanning the NO barcode twice
(the first Scan will be recognised as incorrect item, the second will make the program jump to the next item)

After al lthe items on one order are completed, it will directly follow with the next order.

When all Orders have been processed warehous.py will list unpicked items and completed orders.
you can save this to a protocol file (protocol.txt located in the same folder)
and print it if you want.
Answer the prompts by scanning the YES barcode if you want to save/print.

by default this program does not loop as its intended to be integrated in a standalone solution with other scripts.

