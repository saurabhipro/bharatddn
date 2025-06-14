odoo.define('bharat_ddn.aws_upload_widget', function (require) {
    "use strict";

    const AbstractField = require('web.AbstractField');
    const fieldRegistry = require('web.field_registry');
    const core = require('web.core');
    const QWeb = core.qweb;

    const AWSUploadWidget = AbstractField.extend({
        template: 'AWSUploadWidget',
        events: {
            'change .o_aws_upload_input': '_onFileChange',
            'click .o_aws_upload_button': '_onUploadClick',
        },

        init: function () {
            this._super.apply(this, arguments);
            this.uploading = false;
            this.file = null;
        },

        _render: function () {
            this._super.apply(this, arguments);
            this.$el.html(QWeb.render('AWSUploadWidget', {
                widget: this,
                value: this.value,
            }));
        },

        _onFileChange: function (ev) {
            this.file = ev.target.files[0];
            if (this.file) {
                this._uploadFile();
            }
        },

        _onUploadClick: function () {
            this.$('.o_aws_upload_input').click();
        },

        _uploadFile: function () {
            if (!this.file) return;

            this.uploading = true;
            this._render();

            const formData = new FormData();
            formData.append('file', this.file);
            formData.append('property_id', this.recordData.id);

            this._rpc({
                route: '/api/property/upload_image',
                params: {
                    form_data: formData,
                },
            }).then((result) => {
                if (result.success) {
                    this._setValue(result.url);
                } else {
                    this.do_warn('Error', result.error || 'Upload failed');
                }
            }).catch((error) => {
                this.do_warn('Error', error.message || 'Upload failed');
            }).finally(() => {
                this.uploading = false;
                this._render();
            });
        },
    });

    fieldRegistry.add('aws_upload', AWSUploadWidget);
    return AWSUploadWidget;
}); 