from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from station.views import StationViewSet
from organisation.views import OrganisationViewSet, OrganisationInfoViewSet
from society.views import WorkingSocietyViewSet
from other_group.views import OtherGroupViewSet
from pious_society.views import PiousSocietyViewSet
from lay_apostolate.views import LayApostolateViewSet
from parishioner.views import ParishionerViewSet, ParishionerDataTableViewSet, DeathDetailViewSet
from users.views import UserViewSet
from baptism.views import BaptismViewSet, BaptismDataTableViewSet
from communion.views import CommunionViewSet, CommunionDataTableViewSet
from confirmation.views import ConfirmationViewSet, ConfirmationDataTableViewSet
from matrimony.views import MatrimonyViewSet, MatrimonyDataTableViewSet

router = routers.DefaultRouter()
router.register('station', StationViewSet)
router.register('organisation/info', OrganisationInfoViewSet)
router.register('organisation', OrganisationViewSet)
router.register('society', WorkingSocietyViewSet)
router.register('other_group', OtherGroupViewSet)
router.register('pious_society', PiousSocietyViewSet)
router.register('lay_apostolate', LayApostolateViewSet)
router.register('parishioner/datatable', ParishionerDataTableViewSet)
router.register('parishioner', ParishionerViewSet)
router.register('death_register', DeathDetailViewSet)
router.register('user', UserViewSet)
router.register('sacrament/baptism/datatable', BaptismDataTableViewSet)
router.register('sacrament/baptism', BaptismViewSet)
router.register('sacrament/communion/datatable', CommunionDataTableViewSet)
router.register('sacrament/communion', CommunionViewSet)
router.register('sacrament/confirmation/datatable', ConfirmationDataTableViewSet)
router.register('sacrament/confirmation', ConfirmationViewSet)
router.register('sacrament/matrimony/datatable', MatrimonyDataTableViewSet)
router.register('sacrament/matrimony', MatrimonyViewSet)

urlpatterns = [
  path('api/', include(router.urls)),
  path('', include('church.urls')),
  path('users/', include('users.urls')),
  path('station/', include('station.urls')),
  path('organisation/', include('organisation.urls')),
  path('society/', include('society.urls')),
  path('pious_society/', include('pious_society.urls')),
  path('lay_apostolate/', include('lay_apostolate.urls')),
  path('other_group/', include('other_group.urls')),
  path('parishioner/', include('parishioner.urls')),
  path('priest/', include('priest.urls')),
  path('council/', include('council.urls')),
  path('setting/', include('setting.urls')),
  path('sacrament/baptism/', include('baptism.urls')),
  path('sacrament/communion/', include('communion.urls')),
  path('sacrament/confirmation/', include('confirmation.urls')),
  path('sacrament/matrimony/', include('matrimony.urls')),
  path('admin/', admin.site.urls),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
