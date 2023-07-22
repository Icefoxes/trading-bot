import React from 'react';
import { Avatar, Button, Layout, Menu, Tooltip, Result, Spin, Row, Col } from 'antd';
import { LoginOutlined } from '@ant-design/icons';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { useAuth0 } from "@auth0/auth0-react";
import './layout.scss';
import 'ag-grid-community/styles/ag-grid.css'; // Core grid CSS, always needed
import 'ag-grid-community/styles/ag-theme-alpine.css'; // Optional theme CSS

const { Header, Content, } = Layout;

export const BasicLayout: React.FC = () => {
    const location = useLocation();
    const { loginWithRedirect, logout, isAuthenticated, user, isLoading } = useAuth0();
    if (isLoading) {
        return <div className='auth-loading-container'><Spin size="large" /></div>
    }
    return (
        <Layout className='hades-layout'>
            <Header style={{ display: 'flex', alignItems: 'center', width: '100%', padding: 0 }}>
                <div className='logo' />
                <Menu
                    defaultSelectedKeys={[location.pathname.replace('/', '')]}
                    theme='dark'
                    mode='horizontal'
                    className='layout-header-menus'
                    items={[
                        {
                            key: 'market',
                            label: <Link to='/market' >Market</Link>
                        },
                        {
                            key: 'commission',
                            label: <Link to='/commission' >Commission</Link>
                        },
                        {
                            key: 'backtesting',
                            label: <Link to='/backtesting' >Backtesting</Link>
                        }
                    ]} />
                {isAuthenticated && <Row justify="center" align='middle' className='hades-header-name'>
                    <Col span={4}><Tooltip title='logout'><LoginOutlined style={{ color: 'white' }} onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })} /></Tooltip></Col>
                    <Col span={8}><span className='hades-header-name-text'>{user?.name}</span></Col>
                    <Col span={8}><Avatar src={user?.picture} /></Col>
                </Row>}

            </Header>
            <Content style={{ width: '100%' }}>
                <div className='site-layout-content'>
                    {isAuthenticated && <Outlet />}
                    {!isAuthenticated && <Result
                        status="403"
                        title="403"
                        subTitle="Sorry, you are not authorized to access this page."
                        extra={<Button type="primary" onClick={() => loginWithRedirect()}>Login</Button>}
                    />}
                </div>
            </Content>

        </Layout>
    );
};