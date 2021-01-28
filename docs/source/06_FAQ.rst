FAQ
=====

Error 500: Internal Server Error
---------------------------------
**Error**:

.. code-block:: console

        Error 500: Internal Server Error

The device manager frontend issues a token to a user upon login. The token has an expiration date and is only valid for
X min. If the user is inactive for a longer period of time, the token is not refreshed and access is denied. A token may
invalidate for other reasons as well. Access from multiple browsers by the same user may also cause this issue.

**Solution**: Logout and log back in again. This will renew your token. Close device manager tabs in other browsers.

.. note::  You can set the expiration time and the extension time for a token-refresh in the *backend.py* file in line 87-88.


Protobuf: A file with this name is already in the pool
-------------------------------------------------------
**Error**:

.. code-block:: console

        TypeError: Couldn't build proto file into descriptor pool!
        Invalid proto descriptor for file "messages.proto":
          messages.proto: A file with this name is already in the pool.

This error will show in the backend console and it's logs. It is a known error on windows machines and related to the
protobuf package. The standard wheel installation of protobuf doesn't allow the use of multiple files with the same name
in the same pool. All SiLA devices implement the standard features, thus, this is problematic. The protobuf --no-binary
installation is different to the wheel and allows just that.

**Solution**: Run the *protobuf_no_binary_install.bat* script which is located in the root directory of this software. The
script uninstalls the standard protobuf installation and replaces it with the binary build. Pipenv doesn't implement the
--no-binary flag, thus pip is used. Protobuf is added to the pipfile afterwards for completeness sake.




To-do:
-------
- Incorporate SiLA client meta-data in python repository
- Incorporate observable commands in device manager
- Implement lock/authorization feature
- Edit experiment and update bookings and experiments in backend properly
