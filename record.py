from cortex import Cortex
import time
from threading import Timer

class Record():
    def __init__(self, app_client_id, app_client_secret, **kwargs):
        self.c = Cortex(app_client_id, app_client_secret, debug_mode=True, **kwargs)
        self.c.bind(create_session_done=self.on_create_session_done)
        self.c.bind(create_record_done=self.on_create_record_done)
        self.c.bind(stop_record_done=self.on_stop_record_done)
        self.c.bind(warn_cortex_stop_all_sub=self.on_warn_cortex_stop_all_sub)
        self.c.bind(export_record_done=self.on_export_record_done)
        self.c.bind(inform_error=self.on_inform_error)
        self.headset_found = False
        self.search_timer = None

    def start(self, record_duration_s=20, headsetId='', search_timeout=10):
        print('start record -------------------------')
        self.record_duration_s = record_duration_s
        print('record_duration_s:', record_duration_s)
        if headsetId != '':
            self.c.set_wanted_headset(headsetId)
        print('start authorize -------------------------')
        print('Attempting open')
        
        # Set a timer to stop searching after search_timeout seconds
        self.search_timer = Timer(search_timeout, self.stop_search)
        self.search_timer.start()
        
        self.c.open()

    def stop_search(self):
        if not self.headset_found:
            print("Headset not found within the timeout period.")
            self.c.close()
            self.search_timer = None

    # custom exception hook
    def custom_hook(args):
        print('Custom hook called with args:', args)
        # report the failure
        print(f'Thread failed: {args.exc_value}')

    
    def on_create_session_done(self, *args, **kwargs):
        print('on_create_session_done')
        self.headset_found = True
        if self.search_timer:
            self.search_timer.cancel()
            self.search_timer = None

        # create a record
        self.create_record(self.record_title, description=self.record_description)

    def on_inform_error(self, *args, **kwargs):
        print('on_inform_error')
        error_data = kwargs.get('error_data')
        print(error_data)
        if "queryHeadsets" in str(error_data):
            print("Error querying headsets. Headset might not be connected.")
            self.stop_search()


    def stop_record(self):
        print('stop record -------------------------')
        self.c.stop_record()


    def export_record(self, folder, stream_types, format, record_ids,
                      version, **kwargs):
        """
        To export records
        Parameters
        ----------
        More detail at https://emotiv.gitbook.io/cortex-api/records/exportrecord
        Returns
        -------
        None
        """
        print('export record -------------------------')
        self.c.export_record(folder, stream_types, format, record_ids, version, **kwargs)

    def wait(self, record_duration_s):
        print('wait for recording start -------------------------')
        length = 0
        while length < record_duration_s:
            print('recording at {0} s'.format(length))
            time.sleep(1)
            length+=1
        print('wait for recording end -------------------------')

    def on_create_record_done(self, *args, **kwargs):
        
        data = kwargs.get('data')
        self.record_id = data['uuid']
        start_time = data['startDatetime']
        title = data['title']
        print('on_create_record_done: recordId: {0}, title: {1}, startTime: {2}'.format(self.record_id, title, start_time))

        # record duration is record_length_s
        self.wait(self.record_duration_s)

        # stop record
        self.stop_record()

    def on_stop_record_done(self, *args, **kwargs):
        data = kwargs.get('data')
        record_id = data['uuid']
        start_time = data['startDatetime']
        end_time = data['endDatetime']
        title = data['title']
        print('on_stop_record_done: recordId: {0}, title: {1}, startTime: {2}, endTime: {3}'.format(record_id, title, start_time, end_time))

        # disconnect headset to export record
        print('on_stop_record_done: Disconnect the headset to export record')
        self.c.disconnect_headset()

    def on_warn_cortex_stop_all_sub(self, *args, **kwargs):
        print('on_warn_cortex_stop_all_sub')
        # cortex has closed session. Wait some seconds before exporting record
        time.sleep(3)

        #export record
        self.export_record(self.record_export_folder, self.record_export_data_types,
                           self.record_export_format, [self.record_id], self.record_export_version)

    def on_export_record_done(self, *args, **kwargs):
        print('on_export_record_done: the successful record exporting as below:')
        data = kwargs.get('data')
        print(data)
        self.c.close()


def record_main(record_duration_s: int):
    app_client_id = 'fpCi6nTQcc4Cts2sIAsXNL1xkXOGmIorihpdNbep'
    app_client_secret = '7KBmJhfKAgHvWm9FfMZLaHv3x0EfRERToaRuL3cvJd3JL93ljIZlqD6ndM9UYcT181Okb49m8GRA0oI1Ntanw9VfXC7TqI3440l3aUYNDrJUdw2iduvWQzSbyLu5YAc0'

    r = Record(app_client_id, app_client_secret)

    r.record_title = 'trial'
    r.record_export_folder = '/Users/sanpandey/EEG_Application/recordings/' # your place to export, you should have write permission, example on desktop
    r.record_export_data_types = ['EEG']
    r.record_export_format = 'CSV'
    r.record_export_version = 'V2'
    r.record_description = ''

    record_duration_s = 10
    print('start record_main')
    r.start(record_duration_s)
    print('end record_main')

if __name__ =='__main__':
    record_main()