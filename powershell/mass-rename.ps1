Dir *.md | rename-item -newname { [io.path]::ChangeExtension($_.name, "rst") }