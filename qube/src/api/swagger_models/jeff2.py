from flask_restful_swagger_2 import Schema


class VersionModel(Schema):
    type = 'object'
    properties = {
        'version': {
            'type': 'string',
        }
    }


class jeff2Model(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'string',
        },
        'name': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'tenantId': {
            'type': 'string'
        },
        'orgId': {
            'type': 'string'
        },
        'createdBy': {
            'type': 'string'
        },
        'createdDate': {
            'type': 'string'
        },
        'modifiedBy': {
            'type': 'string'
        },
        'modifiedDate': {
            'type': 'string'
        }
    }
    required = ['name']


class jeff2ModelPost(Schema):
    type = 'object'
    properties = {
        'name': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        }
    }
    required = ['name']


class jeff2ModelPut(Schema):
    type = 'object'
    properties = {
        'name': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        }
    }


class jeff2ModelPostResponse(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'string'
        }
    }


class jeff2ErrorModel(Schema):
    type = 'object'
    properties = {
        'error_code': {
            'type': 'string'
        },
        'error_message': {
            'type': 'string'
        }
    }
    required = ['name']
