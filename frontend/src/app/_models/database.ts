export interface Database {
    id?: number;
    uuid?: string;
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;
}

export interface DatabaseInfo {
    id?: number;
    uuid?: string;
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;
}

export interface DatabaseInfoList {
    data: DatabaseInfo[];
}

export interface DatabaseStatus {
    online: boolean;
    status: string;
}



export const mock_database_info = {
            id: 1,
            title: 'Mock Database 1',
        }

export const mock_database_info_list = [{
            id: 1,
            title: 'Mock Database 1',
        },
        {
            id: 2,
            title: 'Mock Database 2'
        },
        {
            id:3,
            title: 'Mock Database 3'
        }
        ];
