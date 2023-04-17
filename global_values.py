SERVER_PORT_ADDRESS = 'localhost'
SERVER_PORT_NUMBER  = 80
SERVER_IS_UP        = False


SCRAPER_UP          = False


CATEGORY_REGISTRATION = 22
CATEGORY_ATHLETICS    = 12
CATEGORY_CAMPUSORG    = 21
CATEGORY_CLUBS        = 20
CATEGORY_JOBS         = 19


SCRAPER_CATEGORY_FIELDS = {
    "Office of the Registrar": CATEGORY_REGISTRATION,
    "STARFISH":                CATEGORY_REGISTRATION,

    "International Club":                                     CATEGORY_CLUBS,
    "Vulcan Gaming Club":                                     CATEGORY_CLUBS,
    "Cosplay Club":                                           CATEGORY_CLUBS,
    "Chemistry Club":                                         CATEGORY_CLUBS,
    "Office of Military & Veterans Success & Veteran's Club": CATEGORY_CLUBS,
    "Department of Recreation - Club Sports":                 CATEGORY_CLUBS,
    "Forensic Science Club":                                  CATEGORY_CLUBS,
    "SAI":                                                    CATEGORY_CLUBS,


    "Internship Center": CATEGORY_JOBS,
    "TRIO Upward Bound": CATEGORY_JOBS
}


NOTIFICATION_MESSAGE = "No new notifications..."
NOTIFICATION_COUNT   = 0
NOTIFICATION_CODE    = 200
