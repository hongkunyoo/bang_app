from azure.storage.table import TableService, Entity


class Storage(object):

    def __init__(self):
        self.table_service = TableService(account_name='portalvhdsj2ksq9qld7v06',
            account_key='EKOOgf0UchaHBQ25meKH3utLq8bTLZK0fIIwmeXAYlXcTujIlpTkCaycMmkyasMjxUmSpmKTls2hJK7+gV46RA==')
        self.table_name = 'bangs'

    def insert(self, obj):
        try:
            return self.table_service.insert_entity(self.table_name, obj)
        except Exception as e:
            # print(e)
            return None

    # def insert_list(self, objs):
    #     with self.table_service.batch(self.table_name) as batch:
    #         for obj in objs:
    #             try:
    #                 batch.insert_entity(obj)
    #             except Exception as e:
    #                 print(e)

    def get_entity(self, id, seq):
        return self.table_service.get_entity(self.table_name, id, seq)

    def get_entities(self, num_results=None, filter_=None):
        return self.table_service.query_entities(self.table_name, filter=filter_, select=None,
                                                 num_results=num_results, marker=None)
