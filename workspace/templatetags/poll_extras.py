from django import template
from django.db.models import Q
from workspace.models import Crawler, Record, Log

register = template.Library()

@register.simple_tag
def get_crawler_monitor(crawler_id):
    logs = Log.objects.filter(crawler_id=crawler_id)
    ready_logs = logs.filter(status='R')
    pendings_logs = logs.filter(status='P')

    approved_logs = logs.filter(status='A')
    ready_review_jobs = len(ready_logs) + len(pendings_logs)
    ready_import_jobs = len(approved_logs)

    last_log = logs.last()
    last_crawled = ''
    if last_log:
        last_crawled = last_log.run_time

    res = {}
    res['last_crawled'] = last_crawled
    res['ready_review'] = ready_review_jobs
    res['ready_import'] = ready_import_jobs
    return res

@register.simple_tag
def get_log_title(log_id):
    log = Log.objects.get(pk=log_id)
    now = log.run_time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    title = "Job "+str(log.total_record) + " GreenNote "+date_time + " Run Successfully with "+str(log.new_record) + " news/"+str(log.changed_record) + " changes/"+str(log.canceled_record)+" canceled/"+str(log.error_record)+" Errors"
    return title

@register.simple_tag
def get_pending_number_crawler(crawler_id):
    pending_records = Record.objects.filter(crawler_id=int(crawler_id), status='P')
    approved_records = Record.objects.filter(crawler_id=int(crawler_id), status='A')
    total = 0
    if pending_records:
        total += len(pending_records)
    if approved_records:
        total += len(approved_records)
        
    return total


@register.simple_tag
def get_total_number(log_id):
    log = Log.objects.get(pk=log_id)
    crawler_id = log.crawler_id
    records = Record.objects.filter(crawler_id=crawler_id)
    total = 0
    if records:
        total = len(records)

    return total

@register.simple_tag
def get_pending_number(log_id):
    log = Log.objects.get(pk=log_id)
    crawler_id = log.crawler_id
    records = Record.objects.filter(crawler_id=crawler_id, status='P')
    total = 0
    if records:
        total = len(records)
    print(total)

    return total

@register.simple_tag
def get_approved_number(log_id):
    log = Log.objects.get(pk=log_id)
    crawler_id = log.crawler_id
    records = Record.objects.filter(crawler_id=crawler_id, status='A')
    total = 0
    if records:
        total = len(records)

    return total


@register.simple_tag
def get_sent_number(log_id):
    log = Log.objects.get(pk=log_id)
    crawler_id = log.crawler_id
    records = Record.objects.filter(crawler_id=crawler_id, status='S')
    total = 0
    if records:
        total = len(records)

    return total

@register.simple_tag
def get_deleted_number(log_id):
    log = Log.objects.get(pk=log_id)
    crawler_id = log.crawler_id
    records = Record.objects.filter(crawler_id=crawler_id, status='D')
    total = 0
    if records:
        total = len(records)

    return total

@register.simple_tag
def get_canceled_number(log_id):
    log = Log.objects.get(pk=log_id)
    crawler_id = log.crawler_id
    records = Record.objects.filter(crawler_id=crawler_id, status='C')
    total = 0
    if records:
        total = len(records)

    return total

@register.simple_tag
def get_hour(time_str):
    if time_str != "":
        array = time_str.split(":")
        return array[0]
    return ""

@register.simple_tag
def get_min(time_str):
    if time_str != "":
        array = time_str.split(":")
        return array[1]
    return ""



