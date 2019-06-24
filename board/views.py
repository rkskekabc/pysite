from django.db.models import Max, F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from board.models import Board
from pager.pager import Pager

# Create your views here.


def list(request):
    count_per_page = 5
    count_per_block = 5

    try:
        curpage = int(request.GET['page'])
    except Exception:
        curpage = 0

    try:
        kwd = request.POST.get('kwd') or request.GET['kwd']
    except Exception:
        kwd = ''

    page = curpage
    pager = Pager(count_per_page, count_per_block, Board.objects.filter(Q(title__icontains=kwd)|Q(content__icontains=kwd)).count(), page)
    start = page * count_per_page
    list = Board.objects.filter(Q(title__icontains=kwd)|Q(content__icontains=kwd)).order_by('-groupno', '-orderno')[start:start+count_per_page]
    data = {
        'boardlist': list,
        'block_range': range(pager.start_block, pager.end_block + 1),
        'keyword': kwd,
        'pager': pager
    }

    return render(request, 'board/list.html', data)


def writeform(request):
    return render(request, 'board/write.html')


def write(request):
    board = Board()
    value = Board.objects.aggregate(max_groupno=Max('groupno'))
    max_groupno = 0 if value["max_groupno"] is None else value["max_groupno"]

    board.title = request.POST['title']
    board.content = request.POST['content']
    board.hit = 0
    board.groupno = max_groupno + 1
    board.orderno = 1
    board.depth = 0
    board.user_id = request.session['authuser']['id']

    board.save()

    return HttpResponseRedirect('/board')


def delete(request, id=0):
    board = Board.objects.get(id=id)
    board.delete()
    return HttpResponseRedirect('/board')


def view(request, id=0):
    board = Board.objects.get(id=id)
    board.hit += 1
    data = {
        'board': board
    }

    board.save()
    return render(request, 'board/view.html', data)


def modifyform(request, id=0):
    board = Board.objects.get(id=id)
    data = {
        'board': board
    }
    return render(request, 'board/modify.html', data)


def modify(request, id=0):
    board = Board.objects.get(id=id)
    board.title = request.POST['title']
    board.content = request.POST['content']
    board.save()

    return HttpResponseRedirect(f'/board/view/{id}')


def replyform(request, id=0):
    data = {
        'originalid': id
    }
    return render(request, 'board/reply.html', data)


def reply(request, id=0):
    original = Board.objects.get(id=id)

    board = Board()
    board.title = request.POST['title']
    board.content = request.POST['content']
    board.groupno = original.groupno
    board.orderno = original.orderno
    board.depth = original.depth + 1
    board.user_id = request.session['authuser']['id']

    Board.objects.filter(groupno=original.groupno).filter(orderno__gte=original.orderno).update(orderno=F('orderno') + 1)
    board.save()

    return HttpResponseRedirect('/board')
