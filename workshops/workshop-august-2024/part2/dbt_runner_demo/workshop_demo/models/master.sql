select distinct b.id,
    b.url,
    b.node_id,
    b.title,
    b.user__login,
    b.user__id,
    b.created_at,
    b.updated_at,
    b.pull_request__url,
    c1.url as assignee_url,
    c1.login as assignee_login,
    c1.id as assignee_id,
    c2.name as label
from github_data_merge.issues b
left join github_data_merge.issues__assignees c1 on c1._dlt_parent_id = b._dlt_id
left join github_data_merge.issues__labels c2 on c2._dlt_parent_id = b._dlt_id