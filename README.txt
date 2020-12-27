Readme

Requirements
In this project, we try to run the python3 to make our pc as a DNS client which can query an IP address of a domain name. We send the request message to DNS server (8.8.8.8, 53) to ask the IP address. The project can run on a standard Linux machine which only needs libraries: socket, struct, and os. 

Usage
For getting an IP address for a known domain name, there are only two steps, which are running and input, need to be done by running our program. Before running it you should open the terminal for the ubuntu system, and find the path to our program which is my-dns-client.py . 

The first step is inputting "python3 my-dns-client.py" as a command in the terminal to run the program. Then, the screen will prompt you to input the hostname (domain name) which you want to request. Secondly, you can input any correct domain names such as "google.com", "GMU.edu"and so on. It is worth noting that although the DNS server accepts the domain name is without "www", if you input the "www.google.com" in our program, it also can work. Because of considering the habit of daily for the majority the people, we implement this function by a selection statement and an assignment statement. A few moments later, the screen will show all the answer which involves 
	Preparing DNS query..
	...
	Processing DNS response..
	----------------------------------------------------------------------------
	header.ID = <value>
	...
	...
	answer.NAME = <value>
	answer.TYPE = <value>
	...
	...
	answer.RDATA = <value>		## resolved IP address ##

However, if you input a nonexistent domain name, the screen will prompt you 'No such hostname, please check if you entered the correct hostname!'. At the same time, if the computer does not get the response after 5 seconds, it will resend. But, after 3 times, if the computer still can not get the response, it will print an error message like: "Error, This DNS request timeout!"

The last but not least, if the domain name has not only one IP address, our program will show all of them using a loop statement. 
Conclusion:
The program can successfully request the IP address from DNS server (8.8.8.8). we try three domain names: baidu.com, www.google.com, gmu.edu and put the answer in the ANSWER.txt.


