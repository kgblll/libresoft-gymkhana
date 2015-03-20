#
#  Copyright (C) 2009 GSyC/LibreSoft
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
#    Author : Jose Antonio Santos Cadenas <jcaden __at__ gsyc __dot__ es>
#


from django.utils.translation import ugettext_lazy as _, ugettext
from django import forms

from social.core import config

class LoginForm (forms.Form):
        username = forms.CharField(label=_('username'))
        password = forms.CharField(label='password', widget = forms.PasswordInput)
        user = None   # allow access to user object

        def clean(self):
            # only do further checks if the rest was valid
            if self._errors: return

            from django.contrib.auth import authenticate
            user = authenticate(username=self.data['username'],
                                password=self.data['password'])
            if user is not None:
                if user.is_active:
                    self.user = user
                else:
                    raise forms.ValidationError(ugettext(
                        'This account is currently inactive. Please contact '
                        'the administrator if you believe this to be in error.'))
            else:
                raise forms.ValidationError(ugettext(
                    'The username and password you specified are not valid.'))
                
        def login(self, request):
            from django.contrib.auth import login
            if self.is_valid():
                login(request, self.user)
                return self.user.id
            return False

class PhotoForm(forms.Form):
    name = forms.CharField(max_length=30, required=True, label=_('Image name'))
    photo = forms.Field(widget=forms.FileInput,
                        required=False, 
                        label=_('Photo'), 
                        help_text=_('Upload an image (max %s kilobytes)' % config.MAX_PHOTO_UPLOAD_SIZE))

class ComparePhotoForm(forms.Form):
    name = forms.CharField(max_length=30, required=True, label=_('Image name'))
    photo = forms.Field(widget=forms.FileInput,
                        required=False, 
                        label=_('Photo'), 
                        help_text=_('Upload an image (max %s kilobytes)' % config.MAX_PHOTO_UPLOAD_SIZE))


class SoundForm(forms.Form):
    name = forms.CharField(max_length=30, required=True, label=_('Sound file name'))
    sound = forms.Field(widget=forms.FileInput,
                        required=False, 
                        label=_('Sound'), 
                        help_text=_('Upload a sound file'))
    
class VideoForm(forms.Form):
    name = forms.CharField(max_length=30, required=True, label=_('Video file name'))
    video = forms.Field(widget=forms.FileInput,
                        required=False, 
                        label=_('Video'), 
                        help_text=_('Upload a video file(max %s kilobytes)' % config.MAX_VIDEO_UPLOAD_SIZE))
 
class IconForm(forms.Form):
    name = forms.CharField(max_length=30, required=True, label=_('Icon name'))
    icon = forms.Field(widget=forms.FileInput,
                        required=False, 
                        label=_('Icon'), 
                        help_text=_('Upload an image (max %s kilobytes)' % config.MAX_ICON_UPLOAD_SIZE))  
