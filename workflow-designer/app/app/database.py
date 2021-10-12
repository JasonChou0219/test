import logging
import threading
import psycopg2
from psycopg2 import pool
from psycopg2.extras import DictCursor, Json
from classes_proto import Flow, Node, SubFlow


__storage = threading.local()


def get_storage():
    val = getattr(__storage, 'val', None)
    if val is None:
        __storage.val = {}
    return __storage.val


def get_database_connection():
    storage = get_storage()
    if storage.get('pool') is None:
        storage['pool'] = psycopg2.pool.ThreadedConnectionPool(minconn=1,
                                                               maxconn=2000,
                                                               host='localhost',
                                                               port='5432',
                                                               user='postgres',
                                                               password='DIB-central'
                                                               )
    logging.debug('Pool size is:', len(storage['pool']._used))
    for i in range(3):
        try:
            conn = storage['pool'].getconn()
            break
        except Exception as e:
            logging.exception('Pool size is:', len(storage['pool']._used))
            logging.exception(e)
            storage['pool'].closeall()
            continue

    return conn


def release_database_connection(connection):
    storage = get_storage()
    pool = storage.get('pool')
    logging.info('Pool is:', pool)
    logging.info('Pool used connections:', pool._used)

    if pool is not None:
        # Use close=False (default) to increase speed. However, this option will not close but only suspend the
        # connection, indirectly restricting the number of total connections, i.e. devices and users to access.
        # putconn(conn, key=None, close=False)
        pool.putconn(connection, close=True)


def cursor_execute_wrapper(cursor, query_string, vars=None):
    cursor.execute(query_string, vars)


def add_flows_table():
    conn = get_database_connection()
    with conn:
        with conn.cursor() as c:
            try:
                query_string = ('create table if not exists flows'
                                '(id varchar(256) primary key,'
                                'label varchar(256),'
                                'disabled boolean,'
                                'info varchar(256),'
                                'data JSONB)')

                cursor_execute_wrapper(c, query_string)

            except psycopg2.Error as e:
                logging.exception(
                    f'Database error: {e.pgcode}/n SQL: {query_string}\n Error message: {e.pgerror}'
                )
    release_database_connection(conn)


def add_update_flow(flow: Flow) -> None:
    """
    Create a new task entry in the database
    :param flow: The task definition, which is based on the TaskInfo interface
    :return: None
    """
    conn = get_database_connection()
    with conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            query_string = 'INSERT INTO flows VALUES (%s,%s,%s,%s,%s) ON CONFLICT (id) DO UPDATE SET ' \
                           'label = excluded.label,' \
                           'disabled = excluded.disabled,' \
                           'info = excluded.info,' \
                           'data = excluded.data'
            try:
                cursor_execute_wrapper(cursor, query_string, [
                    flow.id, flow.label, flow.disabled,
                    flow.info, Json(flow.data)
                ])
                print(f'Flow with id {flow.id} added to database')
            except psycopg2.Error as e:
                logging.exception(
                    f'Database error: {e.pgcode}/n SQL: {query_string}\n Error message: {e.pgerror}'
                )
    release_database_connection(conn)


def get_flow(flow_flowID: str) -> Flow:
    """
    Get the flow entry (specified by the flowID) from the database
    :param task_uuid: The uuid of the task entry
    :return: The information of the queried task entry according to the TaskInfo interface
    """
    conn = get_database_connection()
    flow = None
    with conn:
        with conn.cursor() as cursor:
            query_string = 'SELECT flowID, label, disabled, info, data FROM flows WHERE flowID=%s'
            try:
                cursor_execute_wrapper(cursor, query_string, [str(flow_flowID)])
                result = cursor.fetchall()
                flow = Flow(id=result[0][0],
                            label=result[0][1],
                            disabled=result[0][2],
                            info=result[0][3],
                            data=result[0][4], )

            except psycopg2.Error as e:
                logging.exception(
                    f'Database error: {e.pgcode}/n SQL: {query_string}\n Error message: {e.pgerror}'
                )
    release_database_connection(conn)
    return flow


def get_flows():
    """
    Get the flows entry (specified by the flowID) from the database
    :param task_uuid: The uuid of the task entry
    :return: The information of the queried task entry according to the TaskInfo interface
    """
    conn = get_database_connection()
    flows = None
    with conn:
        with conn.cursor() as cursor:
            query_string = 'SELECT * FROM nodered'
            try:
                cursor_execute_wrapper(cursor, query_string)
                result = cursor.fetchall()
                flows = result[0][0]

            except psycopg2.Error as e:
                logging.exception(
                    f'Database error: {e.pgcode}/n SQL: {query_string}\n Error message: {e.pgerror}'
                )
    release_database_connection(conn)
    return flows


def add_nodes_table():
    conn = get_database_connection()
    with conn:
        with conn.cursor() as c:
            try:
                query_string = ('create table if not exists nodes'
                                '(id varchar (256) primary key,'
                                'name text,'
                                'type varchar(256),'
                                'x smallint,'
                                'y smallint,'
                                'z varchar(256),'
                                'data text)')

                cursor_execute_wrapper(c, query_string)

            except psycopg2.Error as e:
                logging.exception(
                    f'Database error: {e.pgcode}/n SQL: {query_string}\n Error message: {e.pgerror}'
                )
    release_database_connection(conn)


def add_node(node: Node) -> None:
    """
    Create a new node entry in the database
    :param node: The task definition, which is based on the Node interface
    :return: None
    """
    conn = get_database_connection()
    with conn:
        with conn.cursor() as cursor:
            query_string = 'INSERT INTO nodes VALUES (%s,%s,%s,%s,%s,%s,%s)'
            try:
                cursor_execute_wrapper(cursor, query_string, [
                    node.id, node.name, node.type, node.x,
                    node.y, node.z, node.data
                ])
                print(f'Node with id {node.id} added to database')

            except psycopg2.Error as e:
                logging.exception(
                    f'Database error: {e.pgcode}/n SQL: {query_string}\n Error message: {e.pgerror}'
                )
    release_database_connection(conn)


def get_node(node_nodeID: str) -> Node:
    pass


def add_subflows_table():
    conn = get_database_connection()
    with conn:
        with conn.cursor() as c:
            try:
                query_string = ('create table if not exists subflows'
                                '(id varchar(256) primary key,'
                                'name varchar(256),'
                                'type varchar(256),'
                                'info varchar(256),'
                                'category varchar(256),'
                                'data text)')

                cursor_execute_wrapper(c, query_string)

            except psycopg2.Error as e:
                logging.exception(
                    f'Database error: {e.pgcode}/n SQL: {query_string}\n Error message: {e.pgerror}'
                )
    release_database_connection(conn)


def add_subflow(subflow: SubFlow) -> None:
    """
    Create a new node entry in the database
    :param subflow: The task definition, which is based on the SubFlow interface
    :return: None
    """
    conn = get_database_connection()
    with conn:
        with conn.cursor() as cursor:
            query_string = 'INSERT INTO subflows VALUES (%s,%s,%s,%s,%s,%s)'
            try:
                cursor_execute_wrapper(cursor, query_string, [
                    subflow.id, subflow.name, subflow.type, subflow.info,
                    subflow.category, subflow.data
                ])
                print(f'Node with id {subflow.id} added to database')

            except psycopg2.Error as e:
                logging.exception(
                    f'Database error: {e.pgcode}/n SQL: {query_string}\n Error message: {e.pgerror}'
                )
    release_database_connection(conn)
