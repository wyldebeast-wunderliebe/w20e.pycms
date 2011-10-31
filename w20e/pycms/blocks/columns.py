from base import Group, GroupView


ADD_FORM = """
<form>
  <input type="hidden" name="type" value="columns"/>
  ID: <input type="text" name="id"/><br/>
  Width: <input type="text" name="width"/><br/>
  Height: <input type="text" name="height"/><br/>
  Cols: <input type="text" name="cols"/><br/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""


EDIT_FORM = """
<form>
  <input type="hidden" name="type" value="columns"/>
  <input type="hidden" name="id" value="${data.get('id', '')}"/>
  Width: <input type="text" name="width" value="${data.get('width', '')}"/><br/>
  Height: <input type="text" name="height" value="${data.get('height', '')}"/><br/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""


class ColumnsGroup(Group):

    add_form = ADD_FORM
    edit_form = EDIT_FORM

    type = "columns"


class ColumnGroup(Group):

    type = "column"


class ColumnsGroupView(GroupView):

    pass

