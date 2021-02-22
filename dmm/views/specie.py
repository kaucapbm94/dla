from .default_imports import *
from ..models import Specie


class AddSpecieView(View):

    def post(self, request):
        if request.is_ajax():
            specie_name = request.POST.get('specie_name')
            specie_description = request.POST.get('specie_description')
            specie_expert_id = request.POST.get('specie_expert_id')
            specie_checked_ids = [int(spec_id) for spec_id in json.loads(request.POST.get('specie_checked_ids'))]
            s = Specie(name=specie_name, description=specie_description, expert_id=specie_expert_id)
            logger.info(request.user.expert.name + ' tries to insert specie ' + s.name)
            s.save()
            logger.info(request.user.expert.name + ' successfully inserted specie ' + s.name)
            comment_instance_id = ''
            species = Specie.objects.all()
            species_section = render_to_string('dmm/specie/_specie_section.html',
                                               {'comment_instance_id': comment_instance_id, 'species': species,
                                                'specie_checked_ids': specie_checked_ids})
            return JsonResponse({'species_section': species_section}, status=200)
        return render(request, 'dmm/statistics.html')
