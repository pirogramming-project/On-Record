from django.shortcuts import render,redirect,get_object_or_404
from diaries.models import Diary
from .models import Like,Comment
from django.http import JsonResponse
import json
from django.urls import reverse
from django.db.models import Case, When, BooleanField



def render_communities_main(request):
    diaries = Diary.objects.filter(disclosure = True)
    context = {
        'diaries': diaries
    }
    return render(request, 'communities/communities_main.html', context)

def toggle_like(request, pk):
    diary = Diary.objects.get(id=pk)

    # 좋아요를 추가하거나 가져오기
    get_like, created = Like.objects.get_or_create(diary=diary, like_user=request.user)

    if created:
        # 좋아요가 새로 추가된 경우
        status = 'liked'
    else:
        # 이미 존재하면 삭제하고 'unliked' 반환
        get_like.delete()
        status = 'unliked'

    # 현재 좋아요 개수
    like_count = Like.objects.filter(diary=diary).count()

    # 결과 반환
    return JsonResponse({'like_count': like_count, 'status': status})

def add_comment(request, pk):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            comment_content = body.get('comment', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 JSON 데이터입니다.'}, status=400)

        if not comment_content:
            return JsonResponse({'error': '댓글 내용을 입력하세요.'}, status=400)

        diary = get_object_or_404(Diary, id=pk)
        comment = Comment.objects.create(diary=diary, content=comment_content, comment_user=request.user)

        # 전체 댓글 목록 반환
        whole_comments = Comment.objects.filter(diary=diary).select_related('comment_user').annotate(
            is_author=Case(
                When(comment_user=request.user, then=True),
                default=False,
                output_field=BooleanField()
            )
        )

        comment_list = [
            {
                'id': comment.id,
                'content': comment.content,
                'nickname': comment.comment_user.nickname,
                'delete_url': reverse('communities:delete_comment', kwargs={'pk': comment.id}),
                'is_author': comment.is_author  # 내가 쓴 댓글 여부 추가
            }
            for comment in whole_comments
        ]

        return JsonResponse({'whole_comments': comment_list, 'comment_count': len(comment_list)})

def delete_comment(request,pk):
    target_comment = Comment.objects.get(id=pk)
    target_comment.delete()


    whole_comments = Comment.objects.filter(diary=target_comment.diary).select_related('comment_user').values(
        'id', 'content', 'comment_user__nickname'
    )
    comment_count = whole_comments.count()

    # ajax 구현 염두에 두고 json responser 객체 리턴return JsonResponse({'whole_comments': list(whole_comments), 'comment_count': comment_count})
    return redirect('diaries:detail_diaries', pk=target_comment.diary.pk)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json

def update_comment(request, pk):
    if request.method == 'POST':
        # 댓글 객체 가져오기
        comment = get_object_or_404(Comment, id=pk)

        # 요청 데이터에서 새 댓글 내용 추출
        try:
            body = json.loads(request.body)
            new_content = body.get('content', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 JSON 데이터입니다.'}, status=400)

        # 새 댓글 내용이 비어 있는지 확인
        if not new_content:
            return JsonResponse({'error': '댓글 내용을 입력하세요.'}, status=400)

        # 댓글 업데이트 및 저장
        comment.content = new_content
        comment.save()
        # JSON 응답 반환

        return JsonResponse({
            'id': comment.id,
            'content': comment.content,
            'nickname': comment.comment_user.nickname  # 닉네임 포함
        })

    return JsonResponse({'error': '잘못된 요청입니다.'}, status=405)