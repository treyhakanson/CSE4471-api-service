# CSE 4471 Project API Service

## Overview

The API service managing key distribution and passphrase invalidation for the authentication protocol.

## TODO
* table for users
	* user id
	* email
	* salt
	* hashed + salted password
* table for hashed verification codes
	* foreign key to user
	* hashed + salted passphrase
	* expiration date
* route for login
	* verify passphrase to most recent user hashed verification code.
	* return token signed by the server (verification hash)
