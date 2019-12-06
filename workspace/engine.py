
class Engine:
    def __init__(self):
        pass
    
    def generate_log_detail(self,detail_json):
        '''generating log view text from input list'''
        
        new_list = detail_json['new_list']
        changed_list = detail_json['changed_list']
        canceled_list = detail_json['canceled_list']
        error_list = detail_json['error_list']
        
        new_num = len(new_list)
        changed_num = len(changed_list)
        canceled_num = len(canceled_list)
        error_num = len(error_list)
        total_num = new_num + changed_num + canceled_num + error_num
        detail = 'Crawler Job ID : '+str(detail_json['crawler_id']) + " / Venue : " +detail_json['venue'] + " / Target URL : " + detail_json['domain'] +"\n"
        detail += 'Job Started : ' + detail_json['start_time'] +"\n"
        detail += 'Job Ended : ' + detail_json['end_time'] +"\n"
        detail += "Total records : " + str(total_num) + "\n"
        detail += "\n"
        detail += "New records : " + str(new_num) + "\n"
        
        for record in new_list:
            detail += record + "\n"
        detail += "\n"
        detail += "Changed records : " + str(changed_num) + "\n"

        for record in changed_list:
            detail += record + "\n"
        detail += "\n"
        detail += "Canceled records : " + str(canceled_num) + "\n"

        for record in canceled_list:
            detail += record + "\n"
        detail += "\n"
        detail += "Error records : " + str(error_num) + "\n"

        for record in error_list:
            detail += record + "\n"
        return detail
        