<%inherit file="${context.get('parent_template')}"/>

${parent.name_widget()}

<div class="row">
    ${parent.side_nav()} <br />
    <div class="col-md-10">
        <div class="row">
            <div class="col-md-7 col-md-offset-1">
                ${tmpl_context.wdg.display() | n}
            </div>
        </div>
    </div>
</div>


