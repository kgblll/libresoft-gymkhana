--drop function "get_friends" (integer);

create or replace function "get_friends" (integer) returns setof integer as $$
	declare 
		node_id ALIAS FOR $1;
		row RECORD;
	begin
		for row in select node1_id as id from core_relation where node2_id = node_id and node1_id in 
					(select node2_id from core_relation where node1_id = node_id)
		loop
			return next row.id;
		end loop;
		return;
	end;
$$ LANGUAGE 'plpgsql';

--drop function "get_fof" (integer);

create or replace function "get_fof" (integer) returns setof integer as $$
	declare 
		node_id ALIAS FOR $1;
		row RECORD;
		row2 RECORD;
	begin
		create table f as select id from core_social_node where id in (select * from get_friends(node_id));
		for row in select * from f
		loop
			for row2 in select id from core_social_node where id in (select * from get_friends(row.id)) and (not id in (select * from f))
			loop
				return next row2.id;
			end loop;
		end loop;
		drop table f;
		return;
	end;
$$ LANGUAGE 'plpgsql';

--drop function get_photos_visibles (integer);

create or replace function "get_photos_visibles" (integer) returns setof integer as $$
	declare
		viewer_id ALIAS FOR $1;
		row RECORD;
	begin
		create table friendst as select * from get_friends(viewer_id);
		create table friendsoft as select * from get_fof(viewer_id);
		create table privacy as
			SELECT "core_photo"."uploader_id", "privacy2_privacy".*
				FROM "core_photo" INNER JOIN "privacy2_privacy" 
					ON ("core_photo"."social_node_ptr_id" = "privacy2_privacy"."node_id");
			
		for row in select node_id from privacy where
			(privacy.uploader_id = viewer_id) or
			(privacy.friends_privacy = 3) or
			(privacy.friends_privacy = 2 and uploader_id in (select * from friendsoft)) or
			(privacy.friends_privacy = 1 and uploader_id in (select * from friendst))
		loop
			return next row.node_id;
		end loop;
		drop table friendst;
		drop table friendsoft;
		drop table privacy;
		return;
	end;
$$ LANGUAGE 'plpgsql';

--drop function get_notes_visibles (integer);

create or replace function "get_notes_visibles" (integer) returns setof integer as $$
	declare
		viewer_id ALIAS FOR $1;
		row RECORD;
	begin
		create table friendst as select * from get_friends(viewer_id);
		create table friendsoft as select * from get_fof(viewer_id);
		create table privacy as
			SELECT "core_note"."uploader_id", "privacy2_privacy".*
				FROM "core_note" INNER JOIN "privacy2_privacy" 
					ON ("core_note"."social_node_ptr_id" = "privacy2_privacy"."node_id");
			
		for row in select node_id from privacy where
			(privacy.uploader_id = viewer_id) or
			(privacy.friends_privacy = 3) or
			(privacy.friends_privacy = 2 and uploader_id in (select * from friendsoft)) or
			(privacy.friends_privacy = 1 and uploader_id in (select * from friendst))
		loop
			return next row.node_id;
		end loop;
		drop table friendst;
		drop table friendsoft;
		drop table privacy;
		return;
	end;
$$ LANGUAGE 'plpgsql';

--drop function get_sounds_visibles (integer);

create or replace function "get_sounds_visibles" (integer) returns setof integer as $$
	declare
		viewer_id ALIAS FOR $1;
		row RECORD;
	begin
		create table friendst as select * from get_friends(viewer_id);
		create table friendsoft as select * from get_fof(viewer_id);
		create table privacy as
			SELECT "core_sound"."uploader_id", "privacy2_privacy".*
				FROM "core_sound" INNER JOIN "privacy2_privacy" 
					ON ("core_sound"."social_node_ptr_id" = "privacy2_privacy"."node_id");
			
		for row in select node_id from privacy where
			(privacy.uploader_id = viewer_id) or
			(privacy.friends_privacy = 3) or
			(privacy.friends_privacy = 2 and uploader_id in (select * from friendsoft)) or
			(privacy.friends_privacy = 1 and uploader_id in (select * from friendst))
		loop
			return next row.node_id;
		end loop;
		drop table friendst;
		drop table friendsoft;
		drop table privacy;
		return;
	end;
$$ LANGUAGE 'plpgsql';


--drop function get_videos_visibles (integer);

create or replace function "get_videos_visibles" (integer) returns setof integer as $$
	declare
		viewer_id ALIAS FOR $1;
		row RECORD;
	begin
		create table friendst as select * from get_friends(viewer_id);
		create table friendsoft as select * from get_fof(viewer_id);
		create table privacy as
			SELECT "core_video"."uploader_id", "privacy2_privacy".*
				FROM "core_video" INNER JOIN "privacy2_privacy" 
					ON ("core_video"."social_node_ptr_id" = "privacy2_privacy"."node_id");
			
		for row in select node_id from privacy where
			(privacy.uploader_id = viewer_id) or
			(privacy.friends_privacy = 3) or
			(privacy.friends_privacy = 2 and uploader_id in (select * from friendsoft)) or
			(privacy.friends_privacy = 1 and uploader_id in (select * from friendst))
		loop
			return next row.node_id;
		end loop;
		drop table friendst;
		drop table friendsoft;
		drop table privacy;
		return;
	end;
$$ LANGUAGE 'plpgsql';

--drop function get_persons_visibles (integer);

create or replace function "get_persons_visibles" (integer) returns setof integer as $$
	declare
		viewer_id ALIAS FOR $1;
		row RECORD;
	begin
		create table friendst as select * from get_friends(viewer_id);
		create table friendsoft as select * from get_fof(viewer_id);
		create table privacy as
			SELECT "core_person"."social_node_ptr_id", "privacy2_privacy".*
				FROM "core_person" INNER JOIN "privacy2_privacy" 
					ON ("core_person"."social_node_ptr_id" = "privacy2_privacy"."node_id");
			
		for row in select node_id from privacy where
			(privacy.social_node_ptr_id = viewer_id) or
			(privacy.friends_privacy = 3) or
			(privacy.friends_privacy = 2 and social_node_ptr_id in (select * from friendsoft)) or
			(privacy.friends_privacy = 1 and social_node_ptr_id in (select * from friendst))
		loop
			return next row.node_id;
		end loop;
		drop table friendst;
		drop table friendsoft;
		drop table privacy;
		return;
	end;
$$ LANGUAGE 'plpgsql';


--drop function get_layers_visibles (integer);

create or replace function "get_layers_visibles" (integer) returns setof integer as $$
	declare
		viewer_id ALIAS FOR $1;
		row RECORD;
	begin
		create table friendst as select * from get_friends(viewer_id);
		create table friendsoft as select * from get_fof(viewer_id);
		create table privacy as
			SELECT "core_layer"."uploader_id", "privacy2_privacy".*
				FROM "core_layer" INNER JOIN "privacy2_privacy" 
					ON ("core_layer"."social_node_ptr_id" = "privacy2_privacy"."node_id");
			
		for row in select node_id from privacy where
			(privacy.uploader_id = viewer_id) or
			(privacy.friends_privacy = 3) or
			(privacy.friends_privacy = 2 and uploader_id in (select * from friendsoft)) or
			(privacy.friends_privacy = 1 and uploader_id in (select * from friendst))
		loop
			return next row.node_id;
		end loop;
		drop table friendst;
		drop table friendsoft;
		drop table privacy;
		return;
	end;
$$ LANGUAGE 'plpgsql';






