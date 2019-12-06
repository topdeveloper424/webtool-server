from django.db import models

# Create your models here.

''' model for crawler.  each crawler has one record '''
class Crawler(models.Model):
    PENDING = 'P'
    IMPORTED = 'I'
    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (IMPORTED,'imported'),
    )

    name = models.CharField(max_length=200,unique=True, null = False, default='')
    domain = models.CharField(max_length=255, null = False, default='')
    status = models.CharField(max_length = 4, choices = STATUS_CHOICES, default = PENDING)
    last_import = models.DateTimeField()
    script = models.CharField(max_length=255, null = False, default='')
    running_flag = models.BooleanField(null=False,default=False)


'''model for log. each log has one record.  whenever crawler run job, log will be generated'''
class Log(models.Model):
    READY_FOR_REVIEW = 'P'
    APPROVED = 'A'
    SENT_TO_IMPORT = 'S'
    DELETED = 'D'
    STATUS_CHOICES = (
        (READY_FOR_REVIEW, 'ready for review'),
        (APPROVED, 'approved'),
        (SENT_TO_IMPORT, 'sent to import'),
        (DELETED, 'deleted'),
    )
    status = models.CharField(max_length = 4, choices = STATUS_CHOICES, default = READY_FOR_REVIEW)
    run_time = models.DateTimeField(auto_now_add=True)
    new_record = models.IntegerField(null=False, default=0)
    changed_record = models.IntegerField(null=False, default=0)
    error_record = models.IntegerField(null=False, default=0)
    crawler = models.ForeignKey(Crawler, on_delete=models.CASCADE)
    total_record = models.IntegerField(null=False, default=0)
    canceled_record = models.IntegerField(null=False, default=0)
    detail = models.TextField(blank = True)
    

'''Model for Record. all record comes from crawler job.'''
class Record(models.Model):
    CHANGE = 'C'
    NEW = 'N'
    TYPE_CHOICES = (
        (CHANGE, 'change'),
        (NEW,'new'),
    )

    READY_FOR_REVIEW = 'R'
    APPROVED = 'A'
    EDITED = 'E'
    SENT_TO_IMPORT = 'S'
    CANCELED = 'C'
    STATUS_CHOICES = (
        (READY_FOR_REVIEW, 'ready for review'),
        (EDITED, 'edited'),
        (APPROVED, 'approved'),
        (SENT_TO_IMPORT, 'sent to import'),
        (CANCELED, 'canceled'),
    )

    change_type = models.CharField(max_length = 4, choices = TYPE_CHOICES, default = CHANGE)
    show = models.CharField(max_length=255, null = False, default='')
    date = models.DateField(null = True)
    date_flag = models.BooleanField(null=False, default=False)

    doors = models.CharField(max_length=50, null=True, default='')
    doors_flag = models.BooleanField(null=False, default=False)

    venue = models.CharField(max_length=255, null = False, default='')
    venue_flag = models.BooleanField(null=False, default=False)

    main_act_show_time = models.DateTimeField(null = True)
    main_act_show_time_flag = models.BooleanField(null=False, default=False)

    main_act = models.CharField(max_length=255, null = False, default='')
    main_act_flag = models.BooleanField(null=False, default=False)

    genre = models.CharField(max_length=255, null = True, default='')

    support_act = models.CharField(max_length=255, null = False, default='')
    support_act_flag = models.BooleanField(null=False, default=False)

    show_description = models.TextField()
    show_description_flag = models.BooleanField(null=False, default=False)

    promoter = models.CharField(max_length=255, null = False, default='')
    promoter_flag = models.BooleanField(null=False, default=False)

    festival = models.CharField(max_length=255, null = True, default='')
    festival_flag = models.BooleanField(null=False, default=False)

    info_url = models.CharField(max_length=255, null = True, default='')
    ticket_url = models.CharField(max_length=255, null = True, default='')
    ticket_url_flag = models.BooleanField(null=False, default=False)

    ticket_price = models.FloatField(null = True)
    ticket_price_flag = models.BooleanField(null=False, default=False)

    ticket_onsale_datetime = models.DateTimeField(null = True)
    ticket_onsale_datetime_flag = models.BooleanField(null=False, default=False)

    tickets_at_door_only = models.BooleanField(null=True, default=False)
    tickets_at_door_only_flag = models.BooleanField(null=False, default=False)

    on_sale_soon =  models.BooleanField(null=True, default=False)
    on_sale_soon_flag = models.BooleanField(null=False, default=False)

    free = models.BooleanField(null=True, default=False)
    free_flag = models.BooleanField(null=False, default=False)

    members_onsale_datetime = models.DateTimeField(null = True)
    members_onsale_datetime_flag = models.BooleanField(null=False, default=False)

    sold_out = models.BooleanField(null=False, default=False)
    sold_out_flag = models.BooleanField(null=False, default=False)

    show_type = models.CharField(max_length=20, null = False, default='')
    show_type_flag = models.BooleanField(null=False, default=False)

    listing_main_image = models.TextField(null = False, default='[]')
    listing_main_image_flag = models.BooleanField(null=False, default=False)

    listing_thumbnail = models.CharField(max_length=255, null = False, default='')
    listing_thumbnail_flag = models.BooleanField(null=False, default=False)

    record_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 4, choices = STATUS_CHOICES, default = READY_FOR_REVIEW)
    crawler = models.ForeignKey(Crawler, on_delete=models.CASCADE)



