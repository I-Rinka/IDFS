class task(object):
    def __init__(self, *initial_data, **kwargs):
        self.device_id
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

local_task_type=("null","get_file","post_file","stop")