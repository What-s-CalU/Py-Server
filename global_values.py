SERVER_PORT_ADDRESS = 'localhost'
# SERVER_PORT_ADDRESS = 'http://10.2.90.99'
SERVER_PORT_NUMBER  = 4400

SERVER_IS_UP        = False
SCRAPER_UP          = False
BUTTON_SUPPRESS     = False

NOTIFICATION_MESSAGE         = "No new notifications..."
NOTIFICATION_FOCUSED_MESSAGE = ""
NOTIFICATION_COUNT   = 0
NOTIFICATION_CODE    = 200


# Category Keys (manually entered for faster scraping)
CATEGORY_ACADEMICS    = 22
CATEGORY_ATHLETICS    = 12
CATEGORY_CAMPUSORG    = 21
CATEGORY_CLUBS        = 20
CATEGORY_JOBS         = 19
CATEGORY_HEALTH       = 23
CATEGORY_RELIGION     = 24



SCRAPER_CATEGORY_FIELDS = {

    # Academics
    "Office of the Registrar":             CATEGORY_ACADEMICS,
    "STARFISH":                            CATEGORY_ACADEMICS,
    "Honors Program":                      CATEGORY_ACADEMICS,
    "Peer Mentor Office":                  CATEGORY_ACADEMICS,
    "Cynthia Pascarell, AFSCME President": CATEGORY_ACADEMICS,
    "Student Development":                 CATEGORY_ACADEMICS,
    "New Student Orientation Team":        CATEGORY_ACADEMICS,
    "Student Affairs":                     CATEGORY_ACADEMICS,
    "Commuter Student Services":           CATEGORY_ACADEMICS,
    "Graduate Admissions":                 CATEGORY_ACADEMICS,

    "Center for Student Outreach and Success Coaching": CATEGORY_ACADEMICS,
    "Residence Life and Housing":                       CATEGORY_ACADEMICS,
    "Commuter Student Services":                        CATEGORY_ACADEMICS,
    "University Police & Student Affairs":              CATEGORY_ACADEMICS,
    "Parking and Transportation":                       CATEGORY_ACADEMICS,  
    "Human Resources":                                  CATEGORY_ACADEMICS,
    "Housing/Residence Life":                           CATEGORY_ACADEMICS,
    "Information Technology Services":                  CATEGORY_ACADEMICS,   
    "Vulcan Village":                                   CATEGORY_ACADEMICS,
    "Office of Communications":                         CATEGORY_ACADEMICS,
    "The Office of Diversity, Equity, and Inclusion":   CATEGORY_ACADEMICS,
    "Learning Technology Services":                     CATEGORY_ACADEMICS,
    "Conference Services":                              CATEGORY_ACADEMICS,
    "SOCIAL WORK DEPARTMENT":                           CATEGORY_ACADEMICS,
    "Middle & Secondary Education":                     CATEGORY_ACADEMICS,
    "Communications":                                   CATEGORY_ACADEMICS,
    "PSECU":                                            CATEGORY_ACADEMICS,
    "SAB":                                              CATEGORY_ACADEMICS,
    "BOOKSTORE":                                        CATEGORY_ACADEMICS,
    "Facilities Management":                            CATEGORY_ACADEMICS,
    "Art Department":                                   CATEGORY_ACADEMICS,



    # Clubs
    "International Club":                                                    CATEGORY_CLUBS,
    "Vulcan Gaming Club":                                                    CATEGORY_CLUBS,
    "Cosplay Club":                                                          CATEGORY_CLUBS,
    "Chemistry Club":                                                        CATEGORY_CLUBS,
    "Office of Military & Veterans Success & Veteran's Club":                CATEGORY_CLUBS,
    "Forensic Science Club":                                                 CATEGORY_CLUBS,
    "SAI":                                                                   CATEGORY_CLUBS,
    "PennWest Journalism Society":                                           CATEGORY_CLUBS,
    "PennWest Wildlife Society":                                             CATEGORY_CLUBS,
    "American Democracy Project":                                            CATEGORY_CLUBS,
    "Center for Volunteer Programs and Service Learning":                    CATEGORY_CLUBS,
    "Interdisciplinary Center for Environmental Studies":                    CATEGORY_CLUBS,
    "Vulcan Gaming Club":                                                    CATEGORY_CLUBS,
    "Forensic Science Club":                                                 CATEGORY_CLUBS,
    "Forensic Science Club | Alpha Phi Sigma":                               CATEGORY_CLUBS,
    "Cal Theatre and University Players":                                    CATEGORY_CLUBS,
    "Fraternity and Sorority Life":                                          CATEGORY_CLUBS,

    # Athletic events
    "Department of Recreation":                                              CATEGORY_ATHLETICS,
    "Department of Recreation - Club Sports":                                CATEGORY_ATHLETICS,
    "Vulcan Cheerleaders":                                                   CATEGORY_ATHLETICS,
    "Sport Management":                                                      CATEGORY_ATHLETICS,
    "Women in Sports & Events":                                              CATEGORY_ATHLETICS,


    # Job opportunities
    "Internship Center":                                                      CATEGORY_JOBS,
    "TRIO Upward Bound":                                                      CATEGORY_JOBS,
    "TRIO Upward Bound @ PennWest California":                                CATEGORY_JOBS,
    "Rhonda Gifford - Career Center":                                         CATEGORY_JOBS,
    "College of Natural Sciences and Engineering Technology (Dean's Office)": CATEGORY_JOBS,

    "Vet Tech Program":                 CATEGORY_HEALTH,
    "NOVA CARE REHABILITATION":         CATEGORY_HEALTH,
    "Wellness Services":                CATEGORY_HEALTH,
    "Alcohol and Other Drug Education": CATEGORY_HEALTH,

    # Religious organizations
    "Cal Catholic - Meghan Larsen-Reidy":            CATEGORY_RELIGION,
    "Meghan Larsen-Reidy, Catholic Campus Minister": CATEGORY_RELIGION,
    "STAND Campus Ministry":                         CATEGORY_RELIGION

}
