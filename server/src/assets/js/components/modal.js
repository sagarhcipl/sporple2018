/*
 * Modal functions
 *
 */

module.exports = {

    $modalBg: undefined,
    $modal: undefined,

    currentSuccess: undefined,
    currentNoBtns: undefined,
    transitionDuration: 300,

    _getBgEle: function() {

        //try cache
        var $modalBg = this.$modalBg;

        //if empty, fetch and add to cache
        if(!$modalBg){

            this.$modalBg = $modalBg = $('#modal-bg');
        }

        return $modalBg;
    },

    _getModalEle: function() {

        //try cache
        var $modal = this.$modal;

        //if empty, fetch and add to cache
        if (!$modal) {

            this.$modal = $modal = $('#modal-bg').find('#modal');
        }

        return $modal;
    },

    open: function() {

        var $bg = this._getBgEle();
        var $modal = this._getModalEle();

        $bg.addClass('active'); 
        

        //bind enter key to confirm button
        if (this.currentNoBtns !== true) {

            config.jQEles.$bod.on('keypress', function(e) {

                if(e.keyCode === 13){
                    $modal.children('#modal__confirm').click();
                }
            });
        }
    },

    close: function(self) {

        self = self || this;
        var $bg = self._getBgEle();
        var $modal = this._getModalEle();

        $bg.removeClass('active');

        //remove enter key binding
        config.jQEles.$bod.off('keypress');

        //if video, remove
        if ( $modal.find('iframe').length ) {

            self.reset();
        }

    },

    reset: function() {

        var $modal = this._getModalEle();

        //globals
        self.currentNoBtns = undefined;
        
        $modal
            .attr('class','modal')
            .find('#modal__close').off('click')
            .siblings('h2.ttl').text('')
            .siblings('div.modal__inner').html('')
            .siblings('#modal__confirm').off('click');

        $modal.find('.modal-close').off('click');
        $(document).unbind("keyup");

    },

    refresh: function(html) {
        var $modal = this._getModalEle();
        $modal.find('div.modal__inner').html(html);
    },

    setup: function(html, args) {

        var self = this;
        var $modal = this._getModalEle();
        var startContents = html || '<div class="loading"><i class="fa fa-refresh fa-spin fa-3x fa-fw"></i></div>';
        var options = {
            title: args.title || '',
            classes: args.classes || '',
            contentUrl: args.contentUrl,
            twoBtns: args.twoBtns,
            noBtns: args.noBtns,
            btnText: args.btnText,
            success: args.success,
            callback: args.callback,
        };
        //build class names string
        var cssClasses = options.classes;
        if (options.twoBtns) cssClasses = cssClasses + ' two-btns';
        if (options.noBtns) cssClasses = cssClasses + ' no-btns';

        //set current globals
        self.currentNoBtns = args.noBtns;

        //clear prev content and bindings
        self.reset();

        $modal
            .addClass(cssClasses)
            .find('#modal__close')
                .click(function(e) {
                    //close modal
                    self.close(self);
                })

            .siblings('h2.ttl').text(options.title)

            .siblings('div.modal__inner').append(startContents)

            .siblings('#modal__cancel')
                .click(function(e) {
                    e.preventDefault();

                    //close modal
                    self.close(self);
                })

            .siblings('#modal__confirm')
                .text(options.btnText)
                .click(function(e) {
                    e.preventDefault();

                    //if we have a callback function, call it!
                    if(options.success && typeof(options.success) === 'function') {

                        options.success();
                    
                    }else{

                        //close modal
                        self.close(self);
                    }

                });

        $(document).keyup(function(event){
            if(event.which=='27'){
                self.close();
            }
        });

        //do we need to fetch the proper content?
        if (options.contentUrl) {

            //if we need to load the content at least wait for the open interaction to finish
            var finished = false;
            var minTime = 1500;
            setTimeout(function() {
                finished = true; 
            }, minTime);

            $.get(
                options.contentUrl,
                function(data) {

                    var addContent = function() {

                        $modal.find('div.modal__inner').html(data);

                        $modal.find('.modal-close')
                            .click(function(e) {
                            self.close(self);
                        });

                        //call after form has been setup
                        if(options.callback && typeof(options.callback) === 'function') {

                            //wait for dom to update
                            setTimeout(function() {
                                options.callback();
                            }, 0);
                                    
                        }
                    };

                    //if the timeout has finished then add content
                    var checkFinished = function() {
                        if (finished) {

                            addContent();
                        } else {

                            setTimeout(function() {
                                checkFinished();
                            }, 100);
                        }
                    };

                    checkFinished();

                }
            );

        } else {

            //call after form has been setup
            if(options.callback && typeof(options.callback) === 'function') {

                options.callback();         
            }

        }

    }

};
