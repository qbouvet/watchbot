var Tabs = function($) {
  return {
    
    init: function() {
      this.cacheDom();
      this.setupAria();
      this.appendIndicator();
      this.bindEvents();
    },
    
    cacheDom: function() {
      this.$el = $('.tabs');
      this.$tabList = this.$el.find('ul');
      this.$tab = this.$tabList.find('li');
      this.$tabFirst = this.$tabList.find('li:first-child a');
      this.$tabLink = this.$tab.find('a');
      this.$tabPanel = this.$el.find('section');
      this.$tabPanelFirstContent = this.$el.find('section > *:first-child');
      this.$tabPanelFirst = this.$el.find('section:first-child');
      this.$tabPanelNotFirst = this.$el.find('section:not(:first-of-type)');
    },
    
    bindEvents: function() {
      this.$tabLink.on('click', function(){
        this.changeTab();
        this.animateIndicator($(event.currentTarget));
      }.bind(this));
      this.$tabLink.on('keydown', function() {
        this.changeTabKey();
      }.bind(this));
    },
    
    changeTab: function() {
      var self = $(event.target);
      event.preventDefault();
      this.removeTabFocus();
      this.setSelectedTab(self);
      this.hideAllTabPanels();
      this.setSelectedTabPanel(self);
    },
    
    animateIndicator: function(elem) {
      var offset = elem.offset().left;
      var width = elem.width();    
      var $indicator = this.$tabList.find('.indicator');
      
      console.log(elem.width());
      
      $indicator.transition({ 
        x: offset,
        width: elem.width()
      })
    },
    
    appendIndicator: function() {
      this.$tabList.append('<div class="indicator"></div>');
    },
    
    changeTabKey: function() {
      var self = $(event.target),
        $target = this.setKeyboardDirection(self, event.keyCode);
      
      if ($target.length) {
        this.removeTabFocus(self);
        this.setSelectedTab($target);
      }
      this.hideAllTabPanels();
      this.setSelectedTabPanel($(document.activeElement));
      this.animateIndicator($target);
    },
    
    hideAllTabPanels: function() {
      this.$tabPanel.attr('aria-hidden', 'true');
    },
    
    removeTabFocus: function(self) {
      var $this = self || $('[role="tab"]');
      
      $this.attr({
        'tabindex': '-1',
        'aria-selected': null
      });
    },
    
    selectFirstTab: function() {
      this.$tabFirst.attr({
        'aria-selected': 'true',
        'tabindex': '0'
      });
    },
    
    setupAria: function() {
      this.$tabList.attr('role', 'tablist');
      this.$tab.attr('role', 'presentation');
      this.$tabLink.attr({
        'role': 'tab',
        'tabindex': '-1'
      });
      this.$tabLink.each(function() {
        var $this = $(this);
        
        $this.attr('aria-controls', $this.attr('href').substring(1));
      });
      this.$tabPanel.attr({
        'role': 'tabpanel'
      });
      this.$tabPanelFirstContent.attr({
        'tabindex': '0'
      });
      this.$tabPanelNotFirst.attr({
        'aria-hidden': 'true'
      });
      this.selectFirstTab();
    },
    
    setKeyboardDirection: function(self, keycode) {
      var $prev = self.parents('li').prev().children('[role="tab"]'),
          $next = self.parents('li').next().children('[role="tab"]');
      
      switch (keycode) {
        case 37:
          return $prev;
          break;
        case 39:
          return $next;
          break;
        default:
          return false;
          break;
      }
    },
    
    setSelectedTab: function(self) {
      self.attr({
        'aria-selected': true,
        'tabindex': '0'
      }).focus();
    },
    
    setSelectedTabPanel: function(self) {
      $('#' + self.attr('href').substring(1)).attr('aria-hidden', null);
    },
    
  };
}(jQuery);

Tabs.init();
