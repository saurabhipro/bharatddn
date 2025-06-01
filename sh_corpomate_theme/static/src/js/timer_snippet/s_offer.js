/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

const SHOfferSnippetCountDown = publicWidget.Widget.extend({
    selector: ".js_cls_sh_offer_snippet",
    disabledInEditableMode: true,

    
    
    /**
     * @override
     */
    start: function () {     
        this.$countdownWrapper = this.$('.js_cls_countdown_wrapper');
        
        this.startTime = parseInt(this.el.dataset.startTime);
        this.endTime = parseInt(this.el.dataset.endTime);        
        this._updateTimeLeft();
        this._render();
        this.setInterval = setInterval(this._render.bind(this), 1000);
        return this._super(...arguments);
    },

    
    /**
     * @override
     */

    destroy: function () {
        if (this.setInterval) {
            clearInterval(this.setInterval);
        }
        this._super(...arguments);
    },

    
    /**
     * Updates the remaining time difference.
     *
     * @private
     */

    _updateTimeLeft: function () {
        const currentTimestamp = Date.now() / 1000;
        var delta =  this.endTime - currentTimestamp;
        this.timeLeft = delta;
        this.isFinished = delta < 0;
        this.isStarted = this.startTime <= currentTimestamp;            
    },

    /**
     * Draws the whole countdown
     *
     * @private
     */
    _render: function () {
        this._updateTimeLeft();
        const showCountdown = this.isStarted && !this.isFinished;
        this.$countdownWrapper.toggleClass('d-none', !showCountdown);
        if (showCountdown){ 
            var days = Math.floor(this.timeLeft / 86400);
            var hours = Math.floor((this.timeLeft - days * 86400) / 3600);
            var minutes = Math.floor((this.timeLeft - days * 86400 - hours * 3600) / 60);
            var seconds = Math.floor(this.timeLeft - days * 86400 - hours * 3600 - minutes * 60);
            days = Math.abs(days);

            if (hours < "10") {
                hours = "0" + hours;
            }
            if (minutes < "10") {
                minutes = "0" + minutes;
            }
            if (seconds < "10") {
                seconds = "0" + seconds;
            }

            this.$(".js_cls_days_count").html(days);
            this.$(".js_cls_hours_count").html(hours);
            this.$(".js_cls_minutes_count").html(minutes);
            this.$(".js_cls_seconds_count").html(seconds);
        
        }            
    },
});

publicWidget.registry.SHOfferSnippetCountDown = SHOfferSnippetCountDown;

return SHOfferSnippetCountDown;
