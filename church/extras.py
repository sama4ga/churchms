from django.db import models
from django.utils.translation import gettext_lazy as _
 
class MeetingFreq(models.TextChoices):
  WEEKLY = "Weekly", _("Weekly")
  BIWEEKLY = "BiWeekly", _("Every two weeks")
  MONTHLY = "Monthly", _("Monthly")
  BIMONTHLY = "BiMonthly", _("Every two months")
  QUARTERLY = "Quarterly", _("Every three months")
  BIANNUALLY = "BiAnnually", _("Every six months")
  ANNUALLY = "Annually", _("Annually")
  BIENNIALLY = "Biennially", _("Once every 2 years")

class MeetingDay(models.TextChoices):
  SUNDAY = "Sunday", _("Sunday")
  MONDAY = "Monday", _("Monday")
  TUESDAY = "Tuesday", _("Tuesday")
  WEDNESDAY = "Wednesday", _("Wednesday")
  THURSDAY = "Thursday", _("Thursday")
  FRIDAY = "Friday", _("Friday")
  SATURDAY = "Saturday", _("Saturday")

class MeetingDaySuffix(models.TextChoices):
  NONE = "", _("Select one")
  FIRST = "First", _("First")
  SECOND = "Second", _("Second")
  THIRD = "Third", _("Third")
  FOURTH = "Fourth", _("Fourth")

class Position(models.TextChoices):
  NONE = "", _("Select one")
  PRESIDENT = "President", _("President")
  CHAIRMAN = "Chairman", _("Chairman")
  VICE_PRESIDENT = "VP", _("Vice President")
  VICE_PRESIDENT1 = "VP1", _("Vice President 1")
  VICE_PRESIDENT2 = "VP2", _("Vice President 2")
  VICE_CHAIRMAN = "VC", _("Vice Chairman")
  SECRETARY = "Sect.", _("Secretary")
  ASST_SECRETARY = "Asst. Sect.", _("Assistant Secretary")
  PROVOST1 = "Provost1", _("Provost 1")
  PROVOST2 = "Provost2", _("Provost 2")
  PRO1 = "PRO1", _("PRO 1")
  PRO2 = "PRO2", _("PRO 2")
  TREASURER = "Treasurer", _("Treasurer")
  FINANCIAL_SECRETARY = "Fin. Sect.", _("Financial Secretary")
  CHAPLAIN = "Chaplain", _("Chaplain")
  
class MaritalStatus(models.TextChoices):
  SINGLE = "Single", _("Single")
  MARRIED = "Married", _("Married")
  WIDOWED = "Widowed", _("Widowed")
  DIVORCED = "Divorced", _("Divorced")
  # SEPARATED = "Separated", _("Separated")

class Status(models.TextChoices):
  ACTIVE = "Active", _("Active")
  INACTIVE = "Inactive", _("Inactive")
  SUSPENDED = "Suspended", _("Suspended")
  DOMICILED = "Domiciled", _("Domiciled")
  PROBATION = "Probation", _("Probation")
  # DELETED = "Deleted", _("Deleted")
  # DEAD = "Dead", _("Dead")

class Gender(models.TextChoices):
  MALE = "M", _("Male")
  FEMALE = "F", _("Female")

class Title(models.TextChoices):
  MR = "Mr", _("Mr.")
  MRS = "Mrs", _("Mrs.")
  MS = "Ms", _("Ms.")
  MISS = "Miss", _("Miss.")
  DR = "Dr", _("Dr.")
  PROF = "Prof", _("Prof.")
  ENGR = "Engr", _("Engr.")
