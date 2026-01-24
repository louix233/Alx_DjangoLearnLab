# Permissions & Groups Setup

## Custom Permissions
Added inside Book model:
- can_view
- can_create
- can_edit
- can_delete

## Groups
Created in Django Admin:
- Viewers → can_view
- Editors → can_view, can_create, can_edit
- Admins → all permissions

## Protected Views
book_list      → requires can_view  
create_book    → requires can_create  
edit_book      → requires can_edit
