// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.2.0
// - protoc             v4.25.3
// source: posts.proto

package __

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

// PostsServiceClient is the client API for PostsService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type PostsServiceClient interface {
	CreatePost(ctx context.Context, in *CreateRequest, opts ...grpc.CallOption) (*CreateResponse, error)
	DeletePost(ctx context.Context, in *DeleteRequest, opts ...grpc.CallOption) (*Response, error)
	GetByIdPost(ctx context.Context, in *GetById, opts ...grpc.CallOption) (*Post, error)
	UpdatePost(ctx context.Context, in *UpdateRequest, opts ...grpc.CallOption) (*Response, error)
	GetAllPost(ctx context.Context, in *GetAllRequest, opts ...grpc.CallOption) (*GetAllResponse, error)
}

type postsServiceClient struct {
	cc grpc.ClientConnInterface
}

func NewPostsServiceClient(cc grpc.ClientConnInterface) PostsServiceClient {
	return &postsServiceClient{cc}
}

func (c *postsServiceClient) CreatePost(ctx context.Context, in *CreateRequest, opts ...grpc.CallOption) (*CreateResponse, error) {
	out := new(CreateResponse)
	err := c.cc.Invoke(ctx, "/posts.PostsService/CreatePost", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *postsServiceClient) DeletePost(ctx context.Context, in *DeleteRequest, opts ...grpc.CallOption) (*Response, error) {
	out := new(Response)
	err := c.cc.Invoke(ctx, "/posts.PostsService/DeletePost", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *postsServiceClient) GetByIdPost(ctx context.Context, in *GetById, opts ...grpc.CallOption) (*Post, error) {
	out := new(Post)
	err := c.cc.Invoke(ctx, "/posts.PostsService/GetByIdPost", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *postsServiceClient) UpdatePost(ctx context.Context, in *UpdateRequest, opts ...grpc.CallOption) (*Response, error) {
	out := new(Response)
	err := c.cc.Invoke(ctx, "/posts.PostsService/UpdatePost", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *postsServiceClient) GetAllPost(ctx context.Context, in *GetAllRequest, opts ...grpc.CallOption) (*GetAllResponse, error) {
	out := new(GetAllResponse)
	err := c.cc.Invoke(ctx, "/posts.PostsService/GetAllPost", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// PostsServiceServer is the server API for PostsService service.
// All implementations must embed UnimplementedPostsServiceServer
// for forward compatibility
type PostsServiceServer interface {
	CreatePost(context.Context, *CreateRequest) (*CreateResponse, error)
	DeletePost(context.Context, *DeleteRequest) (*Response, error)
	GetByIdPost(context.Context, *GetById) (*Post, error)
	UpdatePost(context.Context, *UpdateRequest) (*Response, error)
	GetAllPost(context.Context, *GetAllRequest) (*GetAllResponse, error)
	mustEmbedUnimplementedPostsServiceServer()
}

// UnimplementedPostsServiceServer must be embedded to have forward compatible implementations.
type UnimplementedPostsServiceServer struct {
}

func (UnimplementedPostsServiceServer) CreatePost(context.Context, *CreateRequest) (*CreateResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CreatePost not implemented")
}
func (UnimplementedPostsServiceServer) DeletePost(context.Context, *DeleteRequest) (*Response, error) {
	return nil, status.Errorf(codes.Unimplemented, "method DeletePost not implemented")
}
func (UnimplementedPostsServiceServer) GetByIdPost(context.Context, *GetById) (*Post, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetByIdPost not implemented")
}
func (UnimplementedPostsServiceServer) UpdatePost(context.Context, *UpdateRequest) (*Response, error) {
	return nil, status.Errorf(codes.Unimplemented, "method UpdatePost not implemented")
}
func (UnimplementedPostsServiceServer) GetAllPost(context.Context, *GetAllRequest) (*GetAllResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetAllPost not implemented")
}
func (UnimplementedPostsServiceServer) mustEmbedUnimplementedPostsServiceServer() {}

// UnsafePostsServiceServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to PostsServiceServer will
// result in compilation errors.
type UnsafePostsServiceServer interface {
	mustEmbedUnimplementedPostsServiceServer()
}

func RegisterPostsServiceServer(s grpc.ServiceRegistrar, srv PostsServiceServer) {
	s.RegisterService(&PostsService_ServiceDesc, srv)
}

func _PostsService_CreatePost_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(CreateRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(PostsServiceServer).CreatePost(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/posts.PostsService/CreatePost",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(PostsServiceServer).CreatePost(ctx, req.(*CreateRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _PostsService_DeletePost_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(DeleteRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(PostsServiceServer).DeletePost(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/posts.PostsService/DeletePost",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(PostsServiceServer).DeletePost(ctx, req.(*DeleteRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _PostsService_GetByIdPost_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GetById)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(PostsServiceServer).GetByIdPost(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/posts.PostsService/GetByIdPost",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(PostsServiceServer).GetByIdPost(ctx, req.(*GetById))
	}
	return interceptor(ctx, in, info, handler)
}

func _PostsService_UpdatePost_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(UpdateRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(PostsServiceServer).UpdatePost(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/posts.PostsService/UpdatePost",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(PostsServiceServer).UpdatePost(ctx, req.(*UpdateRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _PostsService_GetAllPost_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GetAllRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(PostsServiceServer).GetAllPost(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/posts.PostsService/GetAllPost",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(PostsServiceServer).GetAllPost(ctx, req.(*GetAllRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// PostsService_ServiceDesc is the grpc.ServiceDesc for PostsService service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var PostsService_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "posts.PostsService",
	HandlerType: (*PostsServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "CreatePost",
			Handler:    _PostsService_CreatePost_Handler,
		},
		{
			MethodName: "DeletePost",
			Handler:    _PostsService_DeletePost_Handler,
		},
		{
			MethodName: "GetByIdPost",
			Handler:    _PostsService_GetByIdPost_Handler,
		},
		{
			MethodName: "UpdatePost",
			Handler:    _PostsService_UpdatePost_Handler,
		},
		{
			MethodName: "GetAllPost",
			Handler:    _PostsService_GetAllPost_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "posts.proto",
}
