sudo nano /etc/dhcpcd.conf
uncomment
app.py server starts automaticaly 
On the PC:

Assign a static IP in the same range (e.g., 192.168.1.3) so that it is on the same subnet as the Raspberry Pi.

For Windows: Go to Control Panel > Network and Sharing Center > Change adapter settings. Right-click on the Ethernet connection, select Properties, choose Internet Protocol Version 4 (TCP/IPv4), and set a static IP (e.g., 192.168.1.3).

For Linux: You can set a static IP for the Ethernet connection through the network settings or by editing the configuration file.

Test the Connection:

After assigning static IPs, you can test the connection by running the ping command from the PC:

bash
Copy
Edit
ping 192.168.1.2
You should receive responses from the Raspberry Pi if the connection is successful.

Access the Web Server:

Now, you can open your web browser on the PC and navigate to the Raspberry Pi's IP address (e.g., http://192.168.1.2:5000) to access the web server running on the Raspberry Pi.
