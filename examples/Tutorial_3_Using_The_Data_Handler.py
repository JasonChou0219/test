"""
TUTORIAL 3: Using the Data Handler
---------------------------------------------
3.1 The data handler can be used without writing a script. Go to the data handler tab and setup a database. Influx
    databases are supported. The overview will show you whether a connection has been established between the SiLA 2
    Manager and the specified database. Depending on the security settings of your database, supplying a username or
    password may not be necessary.

3.2 You can link a database to a specific SiLA service. Click on the link button and select the desired database. You
    can unlink a database by selecting the empty option [] in the drop-down menu.

3.3 There are several levels of customization. Expand the Service tree and activate the SiLA Features you want the data-
    acquisition to be active for. Selecting "Data Transfer" on the top level will automatically activate all features.
    Start de-selecting.

3.4 The data handler distinguishes between two types of data: Meta data and process/experimental data. They differ in
    the time interval they are queried in. Both types have a set default polling interval. However, you may customize
    the time interval for both of them for each SiLA Command and Property on the lowest level of the tree.

3.5 If a command requires a parameter, you can set the parameter here.

3.6 The data handler is active for the full duration of the experiment and does not stop when the script is finished.
    It will only stop at the specified time or if the experiment is stopped manually.

Hint 4: If your parameter changes over time, you should exclude the command query from the data handler and add a
    respective function and command call to your experimental script.
"""


def run(services):
    """ Required to import and instantiate devices """
    return
