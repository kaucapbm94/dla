from .default_imports import *

from ..models import Comment, Specie, Tag, TonalType, LanguageType, Result, Expert


class GetInitialsView(View):
    def get(self, request, result_id=None):
        expert_id = request.GET.get('expert_id')
        tag_checked_ids = [int(spec_id) for spec_id in json.loads(request.GET.get('tag_checked_ids'))]
        specie_checked_ids = [int(spec_id) for spec_id in json.loads(request.GET.get('specie_checked_ids'))]
        comment_instance_id = ''
        tags_section = render_to_string(
            'dmm/tag/_tag_section.html',
            {'comment_instance_id': comment_instance_id, 'specific_tags': get_specific_tags(), 'common_tags': get_common_tags(),
             'tag_checked_ids': tag_checked_ids,
             })
        species = Specie.objects.all()
        species_section = render_to_string('dmm/specie/_specie_section.html',
                                           {'comment_instance_id': comment_instance_id, 'species': species,
                                            'specie_checked_ids': specie_checked_ids})

        logger.info(request.user.expert.name +
                    ' starts comment round session ')

        comments_section = ''
        if result_id:
            result = Result.objects.get(id=result_id)
            comments = get_need_round_comments(result, expert_id)
            logger.debug(comments)
            for comment in comments:
                comments_section += render_to_string(
                    'dmm/comment/_round.html', {
                        'comment': comment,
                        'params': comments[comment]
                    })
        else:
            for i in range(1):
                comments_section += render_to_string('dmm/comment/_comment.html',
                                                     {'comment_instance_id': i, 'text': '',
                                                      'parameter_width': parameter_width,
                                                      'label_width': label_width})
        return JsonResponse({
            'tags_section': tags_section,
            'species_section': species_section,
            'comments_section': comments_section,
        }, status=200)


class InsertCommentView(View):
    def post(self, request):
        if request.is_ajax():
            logger.debug(request.POST)
            comment_text = request.POST.get('comment_text')
            author_url = request.POST.get('author_url')
            result_id = request.POST.get('result_id')
            is_answer = (True if request.POST.get('is_answer') in ['true', 'True', 1] else False)
            language_type_id = request.POST.get('language_type_id')
            resource_type_id = request.POST.get('resource_type_id')
            comment_date = pytz.utc.localize(dt.strptime(request.POST.get('comment_date'), '%Y-%m-%dT%H:%M'))
            expert_id = request.POST.get('expert_id')
            create_date = timezone.now()
            expert = Expert.objects.get(id=expert_id)

            c = Comment(
                text=comment_text,
                author_url=author_url,
                result_id=result_id,
                is_answer=is_answer,
                language_type_id=language_type_id,
                resource_type_id=resource_type_id,
                date=comment_date,
                expert_id=expert_id,
                create_date=create_date,
            )
            c.save()
            logger.info(expert.name + ' successfully inserted comment ' + c.text)
            return JsonResponse({'comment_id': c.id}, status=200)
        return render(request, 'dmm/statistics.html')


class GetCommentMetaView(View):
    def get(self, request, result_id=None):
        if request.is_ajax():
            comment_instance_id = request.GET.get('comment_instance_id')

            # tonal_type_section
            tonal_type_checked_id = request.GET.get('tonal_type_checked_ids')
            tonal_types = TonalType.objects.all()
            tonal_type_section = render_to_string('dmm/tonal_type/_tonal_type_section.html',
                                                  {'comment_instance_id': comment_instance_id,
                                                   'tonal_types': tonal_types,
                                                   'tonal_type_checked_ids': tonal_type_checked_id})
            language_type_selected = request.GET.get('language_type_selected')

            # species_section
            species = Specie.objects.all()
            specie_checked_ids = [int(spec_id) for spec_id in json.loads(request.GET.get('specie_checked_ids'))]
            species_section = render_to_string('dmm/specie/_specie_section.html',
                                               {'comment_instance_id': comment_instance_id, 'species': species,
                                                'specie_checked_ids': specie_checked_ids})

            # language_type_section
            language_types = LanguageType.objects.all()
            language_type_section = render_to_string(
                'dmm/language_type/_language_type_section.html',
                {
                    'comment_instance_id': comment_instance_id,
                    'language_types': language_types,
                    'language_type_selected': language_type_selected,
                })

            # tags_section
            tag_checked_ids = [int(spec_id) for spec_id in json.loads(
                request.GET.get('tag_checked_ids'))]
            tags_section = render_to_string(
                'dmm/tag/_tag_section.html',
                {'comment_instance_id': comment_instance_id,
                 'specific_tags': Tag.objects.filter(is_common=False),
                 'common_tags': Tag.objects.filter(is_common=True),
                 'tag_checked_ids': tag_checked_ids
                 })

            comment_date = request.GET.get('comment_date')
            comment_is_answer = (True if request.GET.get(
                'comment_is_answer') in ['true', 'True', 1] else False)
            author_url_value = (
                '' if request.GET.get('author_url_value') is None else request.GET.get('author_url_value'))

            if result_id:
                comment = Comment.objects.get(id=comment_id)
            body = render_to_string(
                'dmm/comment/_form.html', {
                    # 'comment': comment,
                    'comment_instance_id': comment_instance_id,
                    'author_url_value': author_url_value,
                    'comment_date': comment_date,
                    'language_type_section': language_type_section,
                    'comment_is_answer': comment_is_answer,
                    'species_section': species_section,
                    'tonal_type_section': tonal_type_section,
                    'tags_section': tags_section,
                    'result_id': result_id
                })
            return JsonResponse({'body': body}, status=200)
        return render(request, 'dmm/statistics.html')


class AddCommentView(View):
    def get(self, request):
        if request.is_ajax():
            last_comment_id = request.GET.get('last_comment_id')
            # body = get_comment_instance(int(last_comment_id) + 1)
            body = render_to_string(
                'dmm/comment/_comment.html', {
                    'comment_instance_id': int(last_comment_id) + 1,
                    'text': '',
                    'parameter_width': parameter_width,
                    'label_width': label_width
                    # 'comment': comment,
                    # 'params': comments[comment]
                })
            logger.info(request.user.expert.name +
                        ' has requested comment instance')
            return JsonResponse({'body': body}, status=200)
        return render(request, 'dmm/statistics.html')
