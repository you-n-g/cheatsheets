struct Project {
    1: i32 pk,
    2: string project_json,
}

struct ProjectDigest {
    1: i32 pk,
    2: string name,
    3: string award,
    4: string type
}

exception ProjectException {
    1: i32 code,
    2: string name,
    3: string discription
}

service GetProject {
    Project get_project_by_pk(1: i32 pk) throws (1:ProjectException pe);
    list<Project> get_projects_by_pks(1: list<i32> pks) throws (1:ProjectException pe);
    list<ProjectDigest> get_excellent_projects_digest_by_school_pk(1: i32 pk) throws (1:ProjectException pe);
}
