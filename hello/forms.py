from django import forms

class TenantForm(forms.Form):
  ssn = forms.IntegerField(label = 'ssn')
  name = forms.CharField(label = 'tenant_name', max_length = 50)
  phone = forms.IntegerField(label = 'phone_number')
  leasestart = forms.DateField(label = 'lease_start')
  leaseend = forms.DateField(label = 'lease_end')
  leasecopy = forms.CharField(label = 'lease_copy', max_length = 100)
