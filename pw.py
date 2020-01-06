#! /usr/bin/env python

# import sys, os
# from gi.repository import GObject, Gio, Polkit

# def on_tensec_timeout(loop):
#   print("Ten seconds have passed. Now exiting.")
#   loop.quit()
#   return False

# def check_authorization_cb(authority, res, loop):
#     try:
#         result = authority.check_authorization_finish(res)
#         if result.get_is_authorized():
#             print("Authorized")
#         elif result.get_is_challenge():
#             print("Challenge")
#         else:
#             print("Not authorized")
#     except GObject.GError as error:
#          print("Error checking authorization: %s" % error.message)
        
#     print("Authorization check has been cancelled "
#           "and the dialog should now be hidden.\n"
#           "This process will exit in ten seconds.")
#     GObject.timeout_add(10000, on_tensec_timeout, loop)

# def do_cancel(cancellable):
#     print("Timer has expired; cancelling authorization check")
#     cancellable.cancel()
#     return False

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("usage: %s <action_id>" % sys.argv[0])
#         sys.exit(1)
#     action_id = sys.argv[1]

#     mainloop = GObject.MainLoop()
#     authority = Polkit.Authority.get()
#     subject = Polkit.UnixProcess.new(os.getppid())

#     cancellable = Gio.Cancellable()
#     GObject.timeout_add(10 * 1000, do_cancel, cancellable)

#     authority.check_authorization(subject,
#         action_id, #"org.freedesktop.policykit.exec",
#         None,
#         Polkit.CheckAuthorizationFlags.ALLOW_USER_INTERACTION,
#         cancellable,
#         check_authorization_cb,
#         mainloop)

#     mainloop.run()






# import crypt # Interface to crypt(3), to encrypt passwords.
# import getpass # To get a password from user input.
# import spwd # Shadow password database (to read /etc/shadow).

# def login(user, password):
#     """Tries to authenticate a user.
#     Returns True if the authentication succeeds, else the reason
#     (string) is returned."""
#     try:
#         enc_pwd = spwd.getspnam(user)[1]
#         if enc_pwd in ["NP", "!", "", None]:
#             return "user '%s' has no password set" % user
#         if enc_pwd in ["LK", "*"]:
#             return "account is locked"
#         if enc_pwd == "!!":
#             return "password has expired"
#         # Encryption happens here, the hash is stripped from the
#         # enc_pwd and the algorithm id and salt are used to encrypt
#         # the password.
#         if crypt.crypt(password, enc_pwd) == enc_pwd:
#             return True
#         else:
#             return "incorrect password"
#     except KeyError:
#         return "user '%s' not found" % user
#     return "unknown error"

# if __name__ == "__main__":
#     username = raw_input("Username:")
#     password = getpass.getpass()
#     status = login(username, password)
#     if status == True:
#         print("Logged in!")
#     else:
#         print("Login failed, %s." % status)

import PAM
import sys

def is_authorized(username, password):
        """Returns true is a user is authorised via PAM.

        Note: We use the 'login' PAM stack rather than inventing
              our own.

        @rtype: boolean
        """
        pam_auth = None
        try:
            import PAM
            pam_auth = PAM.pam()
        except ImportError:
            log.warn("python-pam is required for XenAPI support.")
            return False
        except NameError:
            # if PAM doesn't exist, let's ignore it
            return False
        
        pam_auth.start("login")
        pam_auth.set_item(PAM.PAM_USER, username)

        def _pam_conv(auth, query_list, user_data = None):
            resp = []
            for i in range(len(query_list)):
                query, qtype = query_list[i]
                if qtype == PAM.PAM_PROMPT_ECHO_ON:
                    resp.append((username, 0))
                elif qtype == PAM.PAM_PROMPT_ECHO_OFF:
                    resp.append((password, 0))
                else:
                    return None
            return resp

        pam_auth.set_item(PAM.PAM_CONV, _pam_conv)
        
        try:
            pam_auth.authenticate()
            pam_auth.acct_mgmt()
        except PAM.error, resp:
            return False
        except Exception, e:
            log.warn("Error with PAM: %s" % str(e))
            return False
        else:
            return True

if __name__ == "__main__":
    if is_authorized(sys.argv[1], sys.argv[2]):
        print("OK - password accepted")
    else:
        print("BAD PASSWORD!!")