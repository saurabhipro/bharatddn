{
    'name':'Mictosite Web',
    'summary':'',
    'description':'',
    'auther':"anjli",
    'website':"example.com",
    'depends': ['base','web','website'],
    'data':[
        # 'security/ir.model.access.csv',
        'views/indore_microsite.xml',

    ],
    'assets':{
        'web.assets_frontend': [
            'microsite/static/src/scss/microsite.scss',
        ],
    },
}